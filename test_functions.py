from fiis_scraping.utils.functions import break_tipo_FII
from pandas.testing import assert_frame_equal
from fiis_scraping.utils.helpers import *

def test_break_tipo_FII():
    df = pd.DataFrame({'tipo_FII': ['Tijolo: Híbrido',
                                     'Abacaxi: Banana',
                                     'Papel: Fundo de Fundos',
                                     np.nan]})
    
    result = break_tipo_FII(df)

    expected = pd.DataFrame({'tipo': ['Tijolo', 'Abacaxi', 'Papel', np.nan],
                             'subtipo':['Híbrido', 'Banana', 'Fundo de Fundos', np.nan]})

    assert_frame_equal(result, expected)