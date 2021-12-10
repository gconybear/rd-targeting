def slider_printout(bounds, m, sd):
    low, up = bounds[0], bounds[1]

    return {'low': round(m - (low*sd), 3), 'up': round(m + (up*sd), 3)} 
