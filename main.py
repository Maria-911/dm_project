import pandas as pd
from itertools import combinations
df = pd.read_csv("data.csv")

def Read_Transactions(df):
    print("Apriori Project")
    data = pd.read_csv("data.csv")
    print("Missing Values:")
    print(data.isnull().sum())

    print(data)

    transactions =[]
    for item in data['items']:
         products = item.split(',')
         products = [x.strip()for x in products]
         products = list(set(products))
         transactions.append(products)
    return transactions

transactions =  Read_Transactions("transactions.csv")

print("Number of Transactions:",len(transactions))

    
print(transactions)

all_items = set()
for transaction in transactions:
  for item in transaction:
    all_items.add(item)
      
print ("Uniqe Items",all_items)
print("Number of Unique Items:",len(all_items))







def get_frequent_1_itemsets(transactions, min_sup):
    n = len(transactions)

    all_items = set()
    for t in transactions:
        all_items.update(t)

    frequent = {}
    for item in all_items:
        count = 0
        for t in transactions:
            if item in t:
                count += 1
        support = count / n
        if support >= min_sup:
            frequent[frozenset([item])] = support

    return frequent


def has_infrequent_subset(candidate, L_prev):
    k = len(candidate)
    for subset in combinations(candidate, k - 1):
        if frozenset(subset) not in L_prev:
            return True
    return False


def generate_candidates(L_prev, k):
    candidates = set()
    for a, b in combinations(list(L_prev.keys()), 2):
        union = a | b
        if len(union) == k and not has_infrequent_subset(union, L_prev):
            candidates.add(union)
    return candidates


def calculate_support(candidates, transactions):
    n = len(transactions)
    support = {}
    for candidate in candidates:
        count = 0
        for t in transactions:
            if candidate <= t:
                count += 1
        support[candidate] = count / n
    return support


def apriori(transactions, min_sup):
    all_levels = {}

    L = get_frequent_1_itemsets(transactions, min_sup)
    k = 1

    while L:
        all_levels[k] = L
        k += 1

        Ck = generate_candidates(L, k)
        support = calculate_support(Ck, transactions)

        L = {}
        for itemset, sup in support.items():
            if sup >= min_sup:
                L[itemset] = sup

    return all_levels


# ---------- Main ----------

df = pd.read_csv("data.csv")
# df = df.drop(columns=["TID"])   # فعّليه فقط لو عندك عمود رقم معاملة (غيّري الاسم)

transactions = []
for _, row in df.iterrows():
    transactions.append({str(x).strip() for x in row if pd.notna(x)})

while True:
    try:
        min_sup = float(input("Enter minimum support (0-1): "))
        if 0 < min_sup <= 1:
            break
        print("Value must be between 0 and 1.")
    except ValueError:
        print("Please enter a number.")

result = apriori(transactions, min_sup)

for k, Lk in result.items():
    print(f"\nL{k}:")
    for itemset, sup in Lk.items():
        print(f"  {set(itemset)}  support = {sup:.2f}")