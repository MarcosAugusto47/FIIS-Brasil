import yaml
from yaml.loader import SafeLoader
from ast import Call, Dict
from typing import Callable, NoReturn
import pandas as pd
from script import df_ifix
import pytest
import numpy as np

@pytest.fixture
def duplicated_ifix() -> pd.DataFrame:
    """
    Get the duplicate rows of the df_ifix
    """
    duplicated_df_ifix = df_ifix[df_ifix.duplicated(subset=['ticker'])]
    return duplicated_df_ifix


def test_duplicate_in_df_ifix(duplicated_ifix: Callable):
    """
    Test if the duplicated dataframe is empty -> no duplicated rows
    """
    assert duplicated_ifix.empty

@pytest.fixture
def ifix_data_types():
    """
    Get the data types of the ifix
    """
    data_types_df_ifix = df_ifix.dtypes.to_dict()

    return data_types_df_ifix

def test_ifix_data_types(ifix_data_types: Callable) -> NoReturn:
    """
    Test the data types of the database and data types of the transformed dataframe
    """
    database_schema_data_types = {'ticker': np.dtype('O'),
                                  'peso': np.dtype('float64'),
                                  'date': np.dtype('O')}

    assert ifix_data_types == database_schema_data_types

@pytest.fixture
def ifix_columns():
    """
    Get the columns of ifix
    """                    
    columns_df_ifix = df_ifix.columns.to_list()
     
    return columns_df_ifix

def test_ifix_columns(ifix_columns: Callable) -> NoReturn:
    """
    Test if the columns of the transformed dataframe match
    the columns of the database
    """
    with open('metadata_ifix.yml') as f:
        database_schema_columns = yaml.load(f, Loader=SafeLoader)['columns']

    assert database_schema_columns == ifix_columns
