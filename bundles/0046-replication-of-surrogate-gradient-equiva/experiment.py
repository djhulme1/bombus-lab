import numpy

DATA = {}

def run(seed: int) -> dict:
    """
    Verifies the claim that the surrogate derivative of a single-neuron Perceptron
    is equivalent to the derivative of the expected output of a stochastic neuron
    if the surrogate matches the derivative of the escape noise function.
    """
    # Setup
    rng = numpy.random.default_rng(seed)
    u_vals = [-1.0, 0.0, 1.0]
    h = 1e-3
    N = 10**7
    
    diff1 = []
    diff2 = []
    
    for u in u_vals:
        # 1. Define the escape noise function p(u) = sigmoid(u)
        p_u = 1.0 / (1.0 + numpy.exp(-u))
        
        # 2. Define the matching surrogate sigma'_1(u) = p'(u) and mismatched sigma'_2(u) = 0.5 p'(u)
        sigma_prime_1 = p_u * (1.0 - p_u)
        sigma_prime_2 = 0.5 * sigma_prime_1
        
        # 4a. Sample N values of noise xi from a Logistic distribution
        # xi = ln(U) - ln(1-U) where U ~ Uniform(0, 1)
        U = rng.random(N)
        xi = numpy.log(U) - numpy.log(1.0 - U)
        
        # 4b. Compute the empirical gradient g_hat(u) using the Common Random Numbers (CRN) method
        # g_hat(u) = 1/(2hN) * sum(I(xi > -u-h) - I(xi > -u+h))
        # We use vectorization for performance
        mask_plus = xi > (-u - h)
        mask_minus = xi > (-u + h)
        g_hat = numpy.sum(mask_plus.astype(float) - mask_minus.astype(float)) / (2.0 * h * N)
        
        # 5. Calculate the absolute difference for the matching surrogate
        diff1.append(abs(g_hat - sigma_prime_1))
        
        # 6. Calculate the absolute difference for the mismatched surrogate
        diff2.append(abs(g_hat - sigma_prime_2))
        
    # 7. Output max_diff as the maximum of diff1(u) across the three u values
    max_diff = float(max(diff1))
    
    # 8. Output target_holds = 1 if max_diff <= 0.02 and mean(diff1) < mean(diff2), otherwise 0
    mean_diff1 = numpy.mean(diff1)
    mean_diff2 = numpy.mean(diff2)
    target_holds = int(1 if (max_diff <= 0.02 and mean_diff1 < mean_diff2) else 0)
    
    return {
        "max_diff": round(max_diff, 10),
        "target_holds": target_holds
    }
