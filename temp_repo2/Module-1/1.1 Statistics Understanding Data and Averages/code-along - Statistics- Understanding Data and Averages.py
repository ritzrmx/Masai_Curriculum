"""
CODE-ALONG (5-10 min) — Academic Session 1
Statistics: Understanding Data and Averages

PROBLEM
-------
Zappy Mart's Udaipur branch reports 7 days of sales (Rs thousands):
    19, 21, 20, 18, 22, 20, 210   <- one day had a huge wedding-season order

The branch manager wants to report "the average daily sales" to head office.

Write code that calculates the MEAN and the MEDIAN from scratch (no
libraries) and decides which one is the more honest number to report.
"""

sales = [19, 21, 20, 18, 22, 20, 210]


# --- SOLUTION -----------------------------------------------------------

def calculate_mean(numbers):
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    ordered = sorted(numbers)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


mean_value = calculate_mean(sales)
median_value = calculate_median(sales)

print(f"Sales data: {sales}")
print(f"Mean   = {mean_value:.1f}")
print(f"Median = {median_value}")

if mean_value - median_value > median_value * 0.2:
    print("-> Mean is far higher than median: an outlier is inflating it.")
    print("-> Report the MEDIAN -- it reflects a typical day.")
else:
    print("-> Mean and median are close: the MEAN is safe to report.")
