expression = "what is (5*5)+3"
import asyncio
import re
from mcptesting import mcptesting

matches = re.findall(r'[\d\.\(\)]+(?:\s*[\+\-\*/]\s*[\d\.\(\)]+)+', expression)
print("MATCHES:", matches)  # ['5*5', '8*8']

if matches:
    for expr in matches:
        expr = expr.strip()
        print("EXPRESSION:", expr)
        result = asyncio.run(mcptesting(expr))
        text = result.content[0].text
        print("RESULT:", text)