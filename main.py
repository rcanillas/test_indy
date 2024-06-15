import json

limit = 10
def aggregate_transactions(file_path):
    transactions_data = []
    with open(file_path,"r") as input_file:
        i = 0
        for transaction_line in input_file:
            transactions_data.append(json.loads(transaction_line))
            i += 1
            if i == limit:
                break
    return transactions_data

def generate_search_grid(threshold,step=1):
    ## Only work with step size >= 1 (no decimals)
    if threshold:
        search_grid = [float(threshold)]
    else: 
        start_value = step
        stop_value = 100
        #print(start_value,stop_value)
        search_grid = [thresh/100 for thresh in range(start_value,stop_value+step,step)]
    #print(search_grid)
    return search_grid

def get_predicted_category(threshold, transaction_line):
    max_probability = 0
    predicted_category = None
    for prediction_category, prediction_probability_string in transaction_line["predictions"].items():
        prediction_probability = float(prediction_probability_string)
        #print(prediction_category, prediction_probability, threshold, max_probability)
        if prediction_probability >= threshold and prediction_probability >= max_probability: 
            ## what if two category have exact probablity ? 
            max_probability = prediction_probability
            predicted_category = prediction_category
    #print(predicted_category)
    return predicted_category

def rate_guess(true_category, predicted_category):
    if true_category == predicted_category:
        match_result = "GoodGuess"
    else:
        match_result = "BadGuess"
    #print(true_category, predicted_category, match_result)
    return match_result

def get_match_result(threshold, transaction_line):
    """
    Si P < Seuil alors on ne prédit aucun compte comptable (NoPred)
    Si P >= Seuil alors:
        - Si le compte prédit est le bon compte, on considère qu'on a une bonne prédiction (GoodGuess)
        - Si le compte prédit n'est pas le bon compte, on a une mauvaise prédiction (BadGuess)
    """
    true_category = transaction_line["true_category"]
    predicted_category = get_predicted_category(threshold, transaction_line)
    if predicted_category:
        match_result = rate_guess(true_category, predicted_category)
    else:
        match_result = "NoPred"
    return match_result

def compute_guess_rate(match_results):
    """PenalizedGoodGuessRate = (GoodGuess - 5 * BadGuess) / (NoPred + GoodGuess + BadGuess)"""
    nb_good_guess = match_results.count("GoodGuess")
    nb_bad_guess = match_results.count("BadGuess")
    penalized_good_guess_rate = (nb_good_guess - 5*nb_bad_guess)/len(match_results)
    print(nb_good_guess,nb_bad_guess,len(match_results),penalized_good_guess_rate)
    return penalized_good_guess_rate


def main(file_path, threshold=None):
    transaction_data = aggregate_transactions(file_path)
    ## below is brutal grid search, possible improvement -> gradient descent / bayesian optimization
    search_grid = generate_search_grid(threshold)
    ## the minimum score is derived from the guess rate formula, worth case scenario. Ideally should be computed from formula. 
    max_penalized_good_guess_rate = -5
    for threshold in search_grid:
        match_results = []
        ## could probably use a pandas dataframe here to make process faster
        for transaction_line in transaction_data:
            transaction_match = get_match_result(threshold, transaction_line)
            match_results.append(transaction_match)
        penalized_good_guess_rate = compute_guess_rate(match_results)
        if penalized_good_guess_rate > max_penalized_good_guess_rate:
            max_penalized_good_guess_rate = penalized_good_guess_rate
        print(threshold, match_results, penalized_good_guess_rate)
    print(max_penalized_good_guess_rate)
    return max_penalized_good_guess_rate


if __name__ == "__main__":
    print("hello")
    #main("predictions.json",0.7)
    print("___________")
    main("predictions.json")
