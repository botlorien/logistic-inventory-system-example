
from typing import List,Tuple
import numpy as np
from array import array

class Route:
    _route:List[Tuple[str,int]]

    def __init__(self) -> None:
        self._route = []
    
    def __repr__(self) -> str:
        return f'Route({self._route!r})'

    def __getitem__(self,index):
        return self._route[index]

    def __iadd__(self,add):
        match add:
            case (str(destiny),int(km)):
                self._route.append(add)
                return self
            case _:
                raise ValueError(
                    f"""Invalid value for route: {add}. Expected tuple(str(destiny),int(km)))"""
                )

    
class Inventory:
    _inventory:List[dict]

    def __init__(self) -> None:
        self._inventory = []

    def __repr__(self) -> str:
        return f'Inventory({self._inventory!r})'

    def __getitem__(self,index):
        return self._inventory[index]

    def __iadd__(self,add):
        match add:
            case {'product':str(product),'stock':int(stock)}:
                self._inventory.append(add)
                return self
            case _:
                raise ValueError(
                    f"""Invalid input value for inventory: {add}. Expected "{{'product':str(product),'stock':int(stock)}}" """
                )

    def __imul__(self,mul):
        if isinstance(mul,(int,float)):
            for item in self._inventory:
                item['stock']*=mul
            return self
        else:
            raise ValueError(
                f'Invalid value for multiplication: {mul}. Expected int(mul) or float(mul)'
            )


    def analyze_stock(self):
        array = np.array(list(item['stock'] for item in self._inventory))
        sum = array.sum()
        mean = np.mean(array)
        std = np.std(array)
        return {'sum':sum, 'mean':mean,'std':std}
    
    def get_stocks_values(self):
        data = array('B',(item['stock'] for item in self._inventory))
        return memoryview(data).tolist()

class LogisticSystem:
    _route:Route
    _inventory:Inventory

    def __init__(self) -> None:
        self._route = None
        self._inventory = None

    def __repr__(self) -> str:
        return f'LogisticSystem({self._inventory!r},{self._route!r})'

    @property
    def route(self):
        return self._route
    
    @route.setter
    def route(self,new):
        if isinstance(new,Route):
            self._route = new
        else:
            raise ValueError(
                f'Invalid type for route: {new}. Expected: Route() instance'
            )

    @property
    def inventory(self):
        return self._inventory
    
    @inventory.setter
    def inventory(self,new):
        if isinstance(new,Inventory):
            self._inventory = new
        else:
            raise ValueError(
                f'Invalid type for inventory: {new}. Expected: Inventory() instance'
            )
    
    def create_routes(self):
        self.route = Route()
        return self.route

    def create_inventory(self):
        self.inventory = Inventory()
        return self.inventory
    
if __name__=='__main__':
    # Criando o system  de logistica
    logistic_system = LogisticSystem()

    # Criando o inventario
    inventory = logistic_system.create_inventory()

    # Criando as rotas
    routes = logistic_system.create_routes()

    # Exibindo os objetos
    print(
        f"""
        inventory: {inventory}
        routes: {routes}
        """
    )

    # Adicionando produtos
    inventory += {"product": "Laptop", "stock": 50}
    inventory += {"product": "Mouse", "stock": 20}

    # Multiplicando o inventary por um fator de 2
    inventory *=2


    # Exibindo o inventario
    print(f'Inventario: {inventory}')

    # Adicionando rotas
    routes += ("Berlin", 300)
    routes += ("Hamburg", 150)

    # Exibindo as rotas
    print(f'Rotas: {routes}')

    # Exibindo as estatisticas do inventario
    print(f'Estatisticas: {inventory.analyze_stock()}')

    # Acessando o primeira rota
    print(f"Primeira rota: {routes[0]}")

    # Acessando o primeiro produto
    print(f"Primeiro produto: {inventory[0]}")

    # Vizualizando todos os valores de estoque do inventario
    print(inventory.get_stocks_values())
