
def rule_b(net_energy, curr_price):
    return net_energy > 0 and curr_price > 0.20 and curr_price < 0.30

def rule_c(net_energy, curr_price):
    return net_energy < 0 and curr_price > 0.40 and curr_price < 0.50
