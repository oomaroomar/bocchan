import subprocess
import asyncio

print('start')
output = subprocess.getoutput('./templogger.sh')
print(output)


async def templogger():
