import random
import math
import random
import math

def f(t, x):
    return x**2


def dfdx(x):
    return 2*x


def d2fdx2(x):
    return 2

def random_sentiment_contribution():
    return random.uniform(-0.01, 0.01)

def ito_lemma(t, x, mu, sigma, f, dfdx, d2fdx2, dW):
    """
    Implements Ito's Lemma for a given function and stochastic process.
    :param t: Current time
    :param x: Current value of the process
    :param mu: Drift term
    :param sigma: Diffusion term
    :param f: Function of (t, x)
    :param dfdx: Partial derivative of f with respect to x
    :param d2fdx2: Second partial derivative of f with respect to x
    :param dW: Increment of Wiener process
    :return: Differential df
    """
    dt = 1e-5
    dft = (mu * dfdx(x) + 0.5 * sigma**2 * d2fdx2(x)) * dt
    dfx = sigma * dfdx(x) * dW
    df = dft + dfx
    return df


def calculate_sentiment_stochastic(text, mu, sigma):
    words = text.split()
    t = 0
    sentiment = 0
    dt = 1
    sentiment_over_time = []


    for word in words:
        score = random_sentiment_contribution()
        dW = random.normalvariate(0, sigma * dt**0.5)
        sentiment_diff = ito_lemma(t, sentiment, mu, sigma, f, dfdx, d2fdx2, dW)
        sentiment += score + sentiment_diff
        sentiment_over_time.append(sentiment)
        t += dt


    return sentiment_over_time



def final_sentiment_score(sentiment_over_time, r, sigma, T):
    S_T = sentiment_over_time[-1]
    K = 0
    d1 = (S_T - K + (r + 0.5 * sigma**2) * T) / (sigma * T**0.5)
    d2 = d1 - sigma * T**0.5


    final_score = S_T * standard_normal_cdf(d1) - K * standard_normal_cdf(d2)
    return final_score


def standard_normal_cdf(x):
    return (1 + math.erf(x / math.sqrt(2))) / 2


def sentiment_analysis_with_stochastic_model(text, mu=0.1, sigma=0.2, r=0.05):
    T = len(text.split())
    sentiment_over_time = calculate_sentiment_stochastic(text, mu, sigma)
    final_score = final_sentiment_score(sentiment_over_time, r, sigma, T)
    return final_score
