from scipy import stats


def get_next_value_in_timeline(x, y):
    slope, intercept, r, p, std_err = stats.linregress(x, y)

    def incline(i):
        return slope * i + intercept

    prediction = list(map(incline, x))

    return round(prediction[-1], 2)


if __name__ == '__main__':
    month = [8, 9, 10]
    # usage_per_month = [8, 9, 10, 11] -> ergebnis 12
    usage_per_month = [30, 30, 50]  # -> 46

    n = get_next_value_in_timeline(month, usage_per_month)
    print(n)
