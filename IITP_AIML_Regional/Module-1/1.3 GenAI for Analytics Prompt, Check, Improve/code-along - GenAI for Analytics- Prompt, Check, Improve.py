"""
CODE-ALONG (5-10 min) — Academic Session 3
GenAI for Analytics: Prompt, Check, Improve

PROBLEM
-------
GenAI summarized Zappy Mart's Kanpur branch week and claimed:
    "Average daily sales were Rs 25,000, showing consistent strong performance."

The real daily sales (Rs thousands) were: 15, 15, 16, 17, 18, 19, 30

Write a simple validator that checks GenAI's claimed number against the
real data, and flags the output as trustworthy or not.
"""

real_sales = [15, 15, 16, 17, 18, 19, 30]
genai_claimed_average = 25.0  # in Rs thousands


# --- SOLUTION -----------------------------------------------------------

def calculate_mean(numbers):
    return sum(numbers) / len(numbers)


def validate_claim(claimed_value, real_numbers, tolerance_percent=10):
    actual_value = calculate_mean(real_numbers)
    difference_percent = abs(claimed_value - actual_value) / actual_value * 100
    is_valid = difference_percent <= tolerance_percent
    return is_valid, actual_value, difference_percent


is_valid, actual_mean, diff_percent = validate_claim(genai_claimed_average, real_sales)

print(f"Real daily sales: {real_sales}")
print(f"GenAI claimed average: Rs {genai_claimed_average}k")
print(f"Actual average:        Rs {actual_mean:.1f}k")
print(f"Difference: {diff_percent:.0f}%")

if is_valid:
    print("-> PASS: claim is close enough to the real data. Safe to use.")
else:
    print("-> FAIL: claim is way off. Re-prompt with the real numbers included.")
