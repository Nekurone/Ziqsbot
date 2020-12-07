from bot import Client
from Core.config import logger, TOKEN

COGS = [
    'owner',
    'roleprotection'
    ]

def main():
    client=Client(COGS)
    logger.GENERAL('Booting Bluebell Core with {0} Cogs.'.format(len(COGS)))
    client.run(TOKEN)

main()
