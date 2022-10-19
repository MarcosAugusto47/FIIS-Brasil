from fiis_scraping.utils.helpers import *

def test_convert_string_to_float():
    df = pd.DataFrame({'x1': ['123,45', 'R$332', '$567,567', '000,0032423', '879.455.667,44']})
    result = convert_string_to_float(df, ['x1']).x1.values
    expected = np.array([123.45, 332, 567.567, 0.0032423, 879455667.44])
    assert np.allclose(result, expected)

def test_convert_percentages_to_float():
    df = pd.DataFrame({'x1': ['%123,45', '332', '%567,567', '000,0032423', '87945']})
    result = convert_percentages_to_float(df, ['x1']).x1.values
    expected = np.array([1.2345, 3.32, 5.6757, 0.0000, 879.45])
    assert np.allclose(result, expected)

def test_convert_to_datetime():
    assert str(convert_to_datetime("15/06/2008")) == '2008-06-15 00:00:00'
    assert np.isnan(convert_to_datetime(444))
    assert np.isnan(convert_to_datetime("abc"))