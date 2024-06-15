import main 

def test_should_generate_search_grid():
    test_threshold = 0.3
    expected_grid = [0.3]
    result_grid = main.generate_search_grid(test_threshold)
    assert expected_grid == result_grid

def test_should_generate_search_grid_with_step_values():
    test_step = 20
    expected_grid = [0.2,0.4,0.6,0.8,1.0]
    result_grid = main.generate_search_grid(None,test_step)
    assert expected_grid == result_grid

def test_should_get_predicted_category():
    test_threshold = 0.3
    test_transaction_line = {"id_transaction": "wAgauXQKA8cYwjXwe",
                            "true_category": "108100",
                            "predictions": {"625300": 0.605,
                                            "625600": 0.034,
                                            "625700": 0.362}}
    expected_category = "625300"
    result_category  = main.get_predicted_category(test_threshold, test_transaction_line)
    assert expected_category == result_category

def test_should_get_no_category():
    test_threshold = 1.0
    test_transaction_line = {"id_transaction": "wAgauXQKA8cYwjXwe",
                            "true_category": "108100",
                            "predictions": {"625300": 0.605,
                                            "625600": 0.034,
                                            "625700": 0.362}}
    expected_category = None
    result_category  = main.get_predicted_category(test_threshold, test_transaction_line)
    assert expected_category == result_category

def test_should_compute_correct_score():
    test_match_results = ["GoodGuess","BadGuess","NoPred"]
    expected_score = (1 - (5*1))/3
    result_score = main.compute_guess_rate(test_match_results)
    assert expected_score == result_score