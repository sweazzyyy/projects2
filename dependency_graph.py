from typing import Dict, List, Set, Tuple
from collections import deque
import time

class DependencyGraph:
    def __init__(self, collector):
        self.collector = collector
        self.graph: Dict[str, List[str]] = {}
        self.visited: Set[str] = set()
        self.cycles: List[List[str]] = []
    
    def build_graph_dfs(self, start_package: str, max_depth: int = None) -> Dict[str, List[str]]:
        """Построение графа зависимостей с помощью DFS без рекурсии"""
        stack = [(start_package, 0)]  # (package, current_depth)
        self.graph = {}
        self.visited = set()
        
        while stack:
            current_package, depth = stack.pop()
            
            # Проверка максимальной глубины
            if max_depth and depth >= max_depth:
                continue
            
            if current_package not in self.visited:
                self.visited.add(current_package)
                
                # Получаем зависимости текущего пакета
                try:
                    if current_package not in self.graph:
                        self.graph[current_package] = []
                    
                    dependencies = self.collector.get_direct_dependencies(current_package)
                    
                    for dep in dependencies:
                        self.graph[current_package].append(dep)
                        
                        # Добавляем зависимость в стек для дальнейшего обхода
                        if dep not in self.visited:
                            stack.append((dep, depth + 1))
                            
                except Exception as e:
                    print(f" Предупреждение: не удалось получить зависимости для {current_package}: {e}")
                    continue
        
        return self.graph
    
    def detect_cycles(self) -> List[List[str]]:
        """Обнаружение циклических зависимостей"""
        self.cycles = []
        visited = set()
        recursion_stack = set()
        path = []
        
        def dfs_cycle_detection(node):
            if node in recursion_stack:
                # Найден цикл
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                if cycle not in self.cycles:
                    self.cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            recursion_stack.add(node)
            path.append(node)
            
            for neighbor in self.graph.get(node, []):
                if neighbor in self.graph:  # Проверяем только пакеты, которые есть в графе
                    dfs_cycle_detection(neighbor)
            
            path.pop()
            recursion_stack.remove(node)
        
        for node in self.graph:
            if node not in visited:
                dfs_cycle_detection(node)
        
        return self.cycles

def build_graph_stage(config: Dict, collector, dependencies: List[str]) -> DependencyGraph:
    """Этап 3: Построение графа зависимостей"""
    graph_builder = DependencyGraph(collector)
    
    print("\nПостроение графа зависимостей")
    
    # Построение графа с помощью DFS
    dependency_graph = graph_builder.build_graph_dfs(config['package_name'])
    
    print(f" Граф построен. Всего узлов: {len(dependency_graph)}")
    
    # Обнаружение циклических зависимостей
    cycles = graph_builder.detect_cycles()
    if cycles:
        print(" Обнаружены циклические зависимости:")
        for i, cycle in enumerate(cycles, 1):
            print(f"  Цикл {i}: {' -> '.join(cycle)} -> {cycle[0]}")
    else:
        print(" Циклические зависимости не обнаружены")
    
    # Демонстрация работы с тестовым репозиторием
    if config.get('test_mode', False):
        print(f"\n Режим тестирования: используется файл {config['test_repo_path']}")
        test_graph = graph_builder.build_graph_dfs(config['package_name'])
        print(f"Тестовый граф: {test_graph}")
    
    return graph_builder