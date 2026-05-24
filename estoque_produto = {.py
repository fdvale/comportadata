estoque_produto = {
   "Arroz": {
       "quantidade": int(input("Digite a quantidade de arroz em estoque: ")),
       "preço": float(input("Digite o preço do arroz: ")),
   },
   "feijão": {
        "quantidade": int(input("Digite a quantidade de feijão em estoque: ")),
        "preço": float(input("Digite o preço do feijão: ")),
   },
   "Batata": {
        "quantidade": int(input("Digite a quantidade de batata em estoque: ")),
        "preço": float(input("Digite o preço da batata: ")),
   }
}
print(estoque_produto)

estoque_produtos = {
    "Arroz": estoque_produto["Arroz"].copy(),
    "feijão": estoque_produto["feijão"].copy(),
    "Batata": estoque_produto["Batata"].copy()
}
    
#se o produto estiver no estoque adicione mais 1, se não estiver, imprima a mensagem "produto não encontrado"
produto = input("Digite o nome do produto que deseja adicionar: ") 
if produto in estoque_produtos:
    estoque_produtos[produto]["quantidade"] += 1
    print(f"Quantidade de {produto} atualizada para {estoque_produtos[produto]['quantidade']}")
else:
    print("Produto não encontrado")

for nome_produto, dados_produto, in estoque_produtos.items(): 
    print(
        f"produto: {nome_produto} - ",
        f"quantidade: {dados_produto['quantidade']} -  ",
        f"preço: {dados_produto['preço']} "
    )

#usando o while para atualizar a quantidade de um produto, por exemplo, se o produto for "Arroz", adicione 1 na quantidade de arroz, se o produto for "feijão", adicione 1 na quantidade de feijão, se o produto for "Batata", adicione 1 na quantidade de batata, se o produto não for encontrado, imprima a mensagem "produto não encontrado"
while True:
    produto = input("Digite o nome do produto que deseja adicionar: ") 
    if produto in estoque_produtos:
        estoque_produtos[produto]["quantidade"] += 1
        print(f"Quantidade de {produto} atualizada para {estoque_produtos[produto]['quantidade']}")
    else:
        print("Produto não encontrado")
    continuar = input("Deseja continuar? (s/n) ")
    if continuar != "s":
        break
