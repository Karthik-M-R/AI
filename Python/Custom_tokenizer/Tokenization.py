import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text="Hey there! i am karthik"
tokens=enc.encode(text)

print("Tokens",tokens)

print('Decoded',enc.decode([25216, 1354, 0, 575, 939, 6490, 404, 507]))


