user_set_profit = 8 #enter as percent
liquidity_limit = 15000  #enter as dollars

ping_alert = 10 #enter as percent
debugMode = False #True/False

token = ''
channel_ID= ''

Iteration_Timer = 60 #number of secconds between each iteration

NAME_ID_CONVERTER = [
    #["ID in coingecko","Name in EnergiSwap"],
    ["energi","Energi"],
    ["dai","Dai Stablecoin"],
    ["ethereum","Ether"],
    ["dogecoin","Dogecoin"],
    ["bitcoin","Bitcoin"],
    ["solana","Solana"],
    ["matic-network","Polygon"],
    ["uniswap","Uniswap"],
    ["ethereum-classic","Ethereum Classic"],
    ["avalanche-2","Avalanche"],
    ["binancecoin","Binance Coin"],
    ["pancakeswap-token","PancakeSwap"],
    ["cardano","Cardano"],
    ["ripple","XRP"],
    ["bittorrent-2","BitTorrent"],
    ["harmony","Harmony"],
    ["fantom","Fantom"],
    ["amp-token","Amp"],
    ["curve-dao-token","Curve DAO"],
    ["bitcoin-cash","Bitcoin Cash"],
    ["holotoken","Holo"],
    ["helium","Helium"],
    ["aave","Aave"],
    ["cosmos","Cosmos"],
    ["yearn-finance","yearn.finance"],
    ["polkadot","Polkadot"],
    ["chainlink","Chainlink"],
    ["filecoin","Filecoin"],
    ["hedera-hashgraph","Hedera Hashgraph"],
    ["omisego","OMG Network"],
    ["1inch","1inch"],
    ["litecoin","Litecoin"],
    ["dash","Dash"],
    ["monero","Monero"],
    ["elrond-erd-2","Elrond"],
    ["algorand","Algorand"],
    ["metal","Metal"],
    ["chiliz","Chiliz"],
    ["kusama","Kusama"],
    ["ftx-token","FTX Token"],
    ["near","Near"],
    ["tron","TRON"],
    ["terra-luna","Terra"],
    ["qtum","Qtum"],
    ["celer-network","Celer Network"],
    ["stellar","Stellar"],
    ["eos","EOS"],
    ["waves","Waves"],
    ["vechain","VeChain"],
    ["decentraland","Decentraland"],
    ["havven","Synthetix"],
    ["wazirx","WazirX"],
    ["neo","Neo"],
    ["yfii-finance","DFI.money"],
    ["gnosis","Gnosis"],
    ["ardor","Ardor"],
    ["maker","Maker"],
    ["basic-attention-token","Basic Attention Token"],
    ["hive","Hive"],
    ["hxro","Hxro"],
    ["polymath","Polymath Network"],
    ["thorchain","THORChain"],
    ["celsius-degree-token","Celsius Network"],
    ["quant-network","Quant"],
    ["cream-2","Cream"],
    ["blockstack","Stacks"],
    ["audius","Audius"],
    ["perpetual-protocol","Perpetual Protocol"],
    ["zencash","Horizen"],
    ["iotex","IoTeX"],
    ["kava","Kava.io"],
    ["iota","IOTA"],
    ["icon","ICON"],
    ["enjincoin","Enjin Coin"],
    ["digibyte","DigiByte"],
    ["iexec-rlc","iExec RLC"],
    ["ankr","Ankr"],
    ["nano","Nano"],
    ["keep3rv1","Keep3rV1"],
    ["celo","Celo"],
    ["theta-token","THETA"],
    ["ark","Ark"],
    ["tezos","Tezos"],
    ["decred","Decred"],
    ["iostoken","IOST"],
    ["ontology","Ontology"],
    ["civic","Civic"],
    ["storj","Storj"],
    ["bancor","Bancor"],
    ["hegic","HEGIC"],
    ["golem","Golem"],
    ["nexo","Nexo"],
    ["nervos-network","Nervos Network"],
    ["aavegotchi","Aavegotchi"],
    ["0x","0x"],
    ["oasis-network","Oasis Network"],
    ["loopring","Loopring"],
    ["zcash","Zcash"],
    ["siacoin","Siacoin"],
    ["ampleforth","Ampleforth"],
    ["ecomi","ECOMI"],
    ["unibright","Unibright"],
    ["compound-governance-token","Compound"],
    ["coti","COTI"],
    ["zilliqa","Zilliqa"],
    ["lisk","Lisk"],
    ["aragon","Aragon"],
    ["balancer","Balancer"],
    ["serum","Serum"],
    ["energy-web-token","Energy Web Token"],
    ["pax-gold","PAX Gold"],
    ["steem","Steem"],
    ["trust-wallet-token","Trust Wallet Token"],
    ["the-sandbox","SAND"],
    ["origin-protocol","Origin Protocol"],
    ["numeraire","Numeraire"],
    ["injective-protocol","Injective Protocol"],
    ["ravencoin","Ravencoin"],
    ["secret","Secret"],
    ["harvest-finance","Harvest Finance"],
    ["certik","CertiK"],
    ["status","Status"],
    ["mask-network","Mask Network"],
    ["maps","MAPS"],
    ["kyber-network","Kyber Network"],
    ["defipulse-index","DeFiPulse Index"],
    ["tellor","Tellor"],
    ["bitshares","BitShares"],
    ["reserve-rights-token","Reserve Rights"],
    ["augur","Augur"],
    ["keep-network","Keep Network"],
    ["aion","Aion"],
    ["rari-governance-token","Rari Governance Token"],
    ["badger-dao","BADGER"],
    ["komodo","Komodo"],
    ["band-protocol","Band Protocol"],
    ["bluzelle","Bluzelle"],
    ["alpha-finance","Alpha Finance"],
    ["republic-protocol","Ren"],
    ["sushi","Sushi"],
    ["rif-token","RSK Infrastructure Framework"],
    ["funfair","FunFair"],
    ["uma","UMA"],
    ["district0x","district0x"],
    ["bzx-protocol","bZx Protocol"],
    ["concierge-io","Travala.com"],
    ["power-ledger","Power Ledger"],
    ["tomochain","Tomochain"],
    ["loom-network-new","Loom"],
    ["ocean-protocol","Ocean Protocol"],
    ["syscoin","Syscoin"],
    ["wanchain","Wanchain"],
    ["dforce-token","dForce Token"],
    ["akropolis","Akropolis"],
    ["orion-protocol","Orion Protocol"],
    ["nexus","Nexus"],
    ["polkastarter","Polkastarter"],
    ["mirror-protocol","Mirror Protocol"],
    ["safepal","SafePal"],
    ["reef-finance","Reef Finance"],
    ["mainframe","Hifi Finance"],
    ["dodo","DODO"],
    ["the-graph","The Graph"],
    ["nucypher","NuCypher"],
    ["xdai-stake","xDAI Stake"],
    ["quark-chain","QuarkChain"],
    ["ferrum-network","Ferrum Network"],
    ["bao-finance","Bao Finance"],
    ["rook","KeeperDAO"],
    ["zkswap","ZKSwap"],
    ["swissborg","SwissBorg"],
    ["rarible","Rarible"],
    ["kava-lend","HARD Protocol"],
    ["nem","NEM"],
    ["dusk-network","DUSK Network"],
    ["trustswap","Trustswap"],
    ["pundi-x","Pundi X"],
    ["populous","Populous"],
    ["redfox-labs-2","RedFOX Labs"],
    ["superfarm","SuperFarm"],
    ["saffron-finance","saffron.finance"]
]

