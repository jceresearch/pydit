"""Module for anonymising a key/identifier column

It applies a randomly generated translation table of integers to the column.
"""
import random
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def anonymise_key(
    df_list,
    key_list,
    map_table_or_dict=None,
    hash_list=None,
    create_new_hash_list=False,
    hash_list_size=1000000,
):
    """Anonymise a column of one or many dataframes with a scrambled list of integers.

    Will persist across the list and it will return the translation table used.

    Parameters
    ----------
    df_list : list of pandas.DataFrame
        List of dataframes to anonymise.
    key_list : list of str
        List of keys to anonymise.
    map_table_or_dict : dict or pandas.DataFrame, optional, default None
        Dictionary or dataframe to use for the translation table.
    hash_list : list of int, optional, default None
        List of integers to use for the translation table.
    create_new_hash_list : bool, optional, default False
        If True, a new list of integers will be created.
    hash_list_size : int, optional, default 1000000
        Size of the hash list to create.

    Returns
    -------
    tuple
        A tuple of the translation table and the hash list.
    """

    def _anonymise(df_list, key_list, map_dict=None, hash_list=None):
        """Internal function to perform the actual anonymisation"""
        master_list = []
        for i, df in enumerate(df_list):
            keys = df[key_list[i]]
            master_list.extend(keys)
        unique_keys = set(master_list)
        print(list(unique_keys))
        if map_dict is None:
            logger.debug("Creating new mapping dictionary")
            map_dict_new = {}
            new_keys = list(unique_keys)
            dummy_keys = list(range(1, len(unique_keys) + 1))
        else:
            map_dict_new = map_dict.copy()
            cur_keys = set(map_dict.keys())
            new_keys = unique_keys - cur_keys
            dummy_keys = list(
                range(len(cur_keys) + 1, len(cur_keys) + len(new_keys) + 1)
            )

        logger.info("New keys count:%s", len(new_keys))
        logger.info("Dummy keys count:%s", len(dummy_keys))
        random.shuffle(dummy_keys)
        add_list = list(zip(new_keys, dummy_keys))
        add_dict = dict(add_list)
        map_dict_new.update(add_dict)
        for i, df in enumerate(df_list):
            if hash_list:
                df[key_list[i] + "_anon"] = df[key_list[i]].map(
                    lambda x: hash_list[map_dict_new[x]]
                )

            else:
                df[key_list[i] + "_anon"] = df[key_list[i]].map(
                    lambda x: map_dict_new[x]
                )

        return map_dict_new

    translation = {}
    if create_new_hash_list:
        hash_list = list(range(1, hash_list_size))
        random.shuffle(hash_list)
        logger.info("Created new hash list")
    if map_table_or_dict is not None:
        if isinstance(map_table_or_dict, dict):
            if (
                isinstance(map_table_or_dict.values()[0], list)
                and len(map_table_or_dict.values()[0]) == 2
            ):
                logger.debug("Stripping previous hash table results")
                clean_dict = {k: map_table_or_dict[k][0] for k in map_table_or_dict}
            elif len(map_table_or_dict.values()[0]) == 1:
                clean_dict = map_table_or_dict.copy()
            else:
                raise ValueError("Mapping dictionary format not recognised, aborting")
        elif isinstance(map_table_or_dict, pd.DataFrame):
            # TODO, do more input validation,
            print(
                "Using ",
                map_table_or_dict.columns[0],
                " as key and ",
                map_table_or_dict.columns[1],
                " as anon key.",
            )
            clean_dict = dict(
                zip(
                    map_table_or_dict[map_table_or_dict.columns[0]],
                    map_table_or_dict[map_table_or_dict.columns[1]],
                )
            )
        else:
            raise TypeError("Object not a dictionary or a dataframe")
    else:
        # no mapping object provided
        clean_dict = None
    translation = _anonymise(df_list, key_list, clean_dict, hash_list)
    if hash_list:
        # The translation is done to hash_list[anon_key] instead of just the
        # random anon_key. This is to further scramble the results esp when we
        # add new items so we need to create that translation table.
        # also we can create a string based ID or some other criteria for a hash
        translation_list = [
            [k, translation[k], hash_list[translation[k]]] for k in translation
        ]
        translation_df = pd.DataFrame(
            data=translation_list, columns=["original_key", "anon_key", "hash_key"]
        )
        logger.info(
            "Finished, returning translation DataFrame and hashtable as separate return values"
        )
        return translation_df, hash_list
    else:
        translation_list = [[k, translation[k]] for k in translation]
        translation_df = pd.DataFrame(
            data=translation_list, columns=["original_key", "anon_key"]
        )
        logger.info("Finished, returning translation DataFrame")
        return translation_df
