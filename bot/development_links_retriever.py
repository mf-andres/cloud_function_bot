def get_development_links():
    links = """
    ## Economy
    Nasdaq:
    https://www.nasdaq.com/market-activity/index/ndx

    GDP:
    https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations=ES

    GDP growth:
    https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=ES

    GDP per capita:
    https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=ES

    GDP per capita growth:
    https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?locations=ES

    GDP inflation:
    https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=ES

    GDP unemployment:
    https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=ES

    GINI:
    https://data.worldbank.org/indicator/GC.DOD.TOTL.GD.ZS?locations=ES&start=1990

    ## World development

    Literacy rate:
    https://data.worldbank.org/indicator/SE.ADT.LITR.ZS

    Mortality rate:
    https://data.worldbank.org/indicator/SH.DYN.MORT

    Internet use rate:
    https://data.worldbank.org/indicator/IT.NET.USER.ZS

    ## Ecological development

    CO2 emissions:
    https://data.worldbank.org/indicator/EN.ATM.CO2E.PC

    Energy use:
    https://data.worldbank.org/indicator/EG.USE.PCAP.KG.OE

    Forest area:
    https://data.worldbank.org/indicator/AG.LND.FRST.ZS

    Agricultural land area:
    https://data.worldbank.org/indicator/AG.LND.AGRI.ZS

    Water stress:
    https://data.worldbank.org/indicator/ER.H2O.FWST.ZS
    """
    print(links)
    return links


if __name__ == "__main__":
    get_development_links()
