""" function for anonymising a key/identifier column applying a randomly generated
translation table of integers
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
    """Function to anonymise a column of one or many dataframes. by a
    the values with a scrambled list of integers. Will persist across the list
    and it will return the translation table used, 

    Args:
        df_list (_type_): _description_
        key_list (_type_): _description_
        map_table_or_dict (_type_, optional): _description_. Defaults to None.
        hash_list (_type_, optional): _description_. Defaults to None.
        create_new_hash_list (bool, optional): _description_. Defaults to False.
        hash_list_size (int, optional): _description_. Defaults to 1000000.
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
            print("Creating new mapping dictionary")
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

        print("New keys count:", len(new_keys))
        print("Dummy keys count:", len(dummy_keys))
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
        print("Created new hash list")
    if map_table_or_dict is not None:
        if isinstance(map_table_or_dict, dict):
            if (
                isinstance(map_table_or_dict.values()[0], list)
                and len(map_table_or_dict.values()[0]) == 2
            ):
                print("Debug: Stripping previous hash table results")
                clean_dict = {k: map_table_or_dict[k][0] for k in map_table_or_dict}
            elif len(map_table_or_dict.values()[0]) == 1:
                clean_dict = map_table_or_dict.copy()
            else:
                print("Mapping dictionary format not recognised, aborting")
                return
        elif isinstance(map_table_or_dict, pd.DataFrame):
            # TODO, probably worth doing more checks about the data coming,
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
            print(
                "Mapping object provided is not a Dictionary or a Dataframe, aborting"
            )
            return
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
        print(
            "Finished, returning translation DataFrame and hashtable as separate return values"
        )
        return translation_df, hash_list
    else:
        translation_list = [[k, translation[k]] for k in translation]
        translation_df = pd.DataFrame(
            data=translation_list, columns=["original_key", "anon_key"]
        )
        print("Finished, returning translation DataFrame")
        return translation_df
