from streamlit.testing.v1 import AppTest


def test_main():
    main_location = "main.py"

    main = AppTest.from_file(main_location, default_timeout=999)
    main.run(timeout=None)
    assert main is not None


# def test__main_title():
#     main_location = "main.py"

#     main = AppTest.from_file(main_location, default_timeout=999)
#     main.run(timeout=None)
#     assert main.title.len == 1
