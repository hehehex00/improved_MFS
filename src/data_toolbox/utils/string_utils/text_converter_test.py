import pandas as pd

from .text_converter import TextConverter


def test_methods_exist_text_converter():
    """ Test to check if all necessary methods exist in the TextConverter class """
    assert hasattr(TextConverter(), 'text_to_df')

def test_text_to_df_empty_text():
    text = ""
    expected_df = pd.DataFrame({"Word": []})
    result_df = TextConverter.text_to_df(text)
    pd.testing.assert_frame_equal(result_df, expected_df)
    
def test_text_to_df_single_word():
    text = "Hello"
    expected_df = pd.DataFrame({"Word": ["Hello"]})
    result_df = TextConverter.text_to_df(text)
    pd.testing.assert_frame_equal(result_df, expected_df)
    
def test_text_to_df_multiple_words():
    text = "This is a test"
    expected_df = pd.DataFrame({"Word": ["This", "is", "a", "test"]})
    result_df = TextConverter.text_to_df(text)
    pd.testing.assert_frame_equal(result_df, expected_df)
    
def test_text_to_df_invalid_characters():
    text = "This is a test with special characters: !@#"
    expected_df = pd.DataFrame({"Word": ["This", "is", "a", "test", "with", "special", "characters"]})
    result_df = TextConverter.text_to_df(text)
    pd.testing.assert_frame_equal(result_df, expected_df)
    
def test_text_to_df_mixed_cases():
    text = "This is A MixEd CAsE"
    expected_df = pd.DataFrame({"Word": ["This", "is", "A", "MixEd", "CAsE"]})
    result_df = TextConverter.text_to_df(text)
    pd.testing.assert_frame_equal(result_df, expected_df)
