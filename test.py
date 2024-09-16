from main import *


companyList = """无锡市建设发展投资有限公司
淮安市投资控股集团有限公司"""


if __name__ == "__main__":
    server_ip = None
    server_port = None

    proxies = set_proxies(server_ip = server_ip,
                server_port = server_port)

    tyc = TYC(proxies=proxies)
    
    tyc.new_session()
    
    for companyName in companyList.split("\n"):
        graphId = tyc.search(companyName)
        table = tyc.fetch_basic(graphId)
        print(table)
        time.sleep(3)
