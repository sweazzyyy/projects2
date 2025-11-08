from typing import List, Dict, Set
from collections import deque, defaultdict

class GraphOperations:
    def __init__(self, graph: Dict[str, List[str]]):
        self.graph = graph
        self.reverse_graph = self._build_reverse_graph()
    
    def _build_reverse_graph(self) -> Dict[str, List[str]]:
        """Построение обратного графа для поиска обратных зависимостей"""
        reverse = defaultdict(list)
        for package, dependencies in self.graph.items():
            for dep in dependencies:
                reverse[dep].append(package)
        return dict(reverse)
    
    def get_load_order(self, package: str) -> List[str]:
        """Получение порядка загрузки зависимостей (топологическая сортировка)"""
        in_degree = defaultdict(int)
        
        # Вычисляем входящие степени
        for node in self.graph:
            for neighbor in self.graph.get(node, []):
                in_degree[neighbor] += 1
            if node not in in_degree:
                in_degree[node] = 0
        
        # Алгоритм Кана для топологической сортировки
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        load_order = []
        
        while queue:
            current = queue.popleft()
            load_order.append(current)
            
            for neighbor in self.graph.get(current, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(load_order) != len(in_degree):
            print(" В графе есть циклы, полная топологическая сортировка невозможна")
        
        return load_order
    
    def get_reverse_dependencies(self, package: str) -> List[str]:
        """Получение обратных зависимостей (какие пакеты зависят от данного)"""
        return self.reverse_graph.get(package, [])
    
    def compare_with_actual_manager(self, package: str):
        """Сравнение с реальным менеджером пакетов"""
        our_order = self.get_load_order(package)
        
        print(f"\n Сравнение порядка загрузки для '{package}':")
        print(f"Наш порядок ({len(our_order)} пакетов):")
        for i, pkg in enumerate(our_order[:10], 1):  # Показываем первые 10
            print(f"  {i}. {pkg}")
        
        if len(our_order) > 10:
            print(f"  ... и еще {len(our_order) - 10} пакетов")
        
        # Здесь можно добавить реальное сравнение с pip
        print("\n Примечание: для точного сравнения с pip можно использовать:")
        print("   pip show <package> или pipdeptree")

def additional_operations_stage(graph: Dict[str, List[str]], config: Dict):
    """Этап 4: Дополнительные операции над графом"""
    operations = GraphOperations(graph)
    
    print("\nДополнительные операции")
    
    # Порядок загрузки зависимостей
    load_order = operations.get_load_order(config['package_name'])
    print(f" Порядок загрузки зависимостей для '{config['package_name']}':")
    for i, package in enumerate(load_order, 1):
        print(f"  {i}. {package}")
    
    # Сравнение с реальным менеджером пакетов
    operations.compare_with_actual_manager(config['package_name'])
    
    # Обратные зависимости
    reverse_deps = operations.get_reverse_dependencies(config['package_name'])
    if reverse_deps:
        print(f"\n Пакеты, зависящие от '{config['package_name']}':")
        for dep in reverse_deps:
            print(f"  - {dep}")
    else:
        print(f"\n Нет пакетов, зависящих от '{config['package_name']}'")
    
    return operations