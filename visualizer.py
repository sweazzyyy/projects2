import subprocess
import os
import tempfile
from typing import Dict, List  # Добавлен импорт List

class GraphVisualizer:
    def __init__(self):
        self.check_d2_installation()
    
    def check_d2_installation(self):
        """Проверка установки D2"""
        try:
            subprocess.run(['d2', '--version'], capture_output=True, check=True)
            print("✅ D2 найден")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ D2 не установлен. Для установки выполните:")
            print("   curl -fsSL https://d2lang.com/install.sh | sh")
            print("   Или скачайте с: https://d2lang.com/")
            # Временно отключаем ошибку для тестирования
            print("  Продолжаем без D2...")
    
    def generate_d2_script(self, graph: Dict[str, List[str]], package_name: str) -> str:
        """Генерация D2 скрипта для визуализации графа"""
        d2_script = f"""direction: right

{package_name} {{
    style: {{
        fill: "#ff6b6b"
        bold: true
    }}
}}
"""
        
        # Добавляем все узлы и связи
        added_nodes = set([package_name])
        
        for package, dependencies in graph.items():
            if package not in added_nodes:
                d2_script += f'{package} {{\n    style: {{\n        fill: "#4ecdc4"\n    }}\n}}\n'
                added_nodes.add(package)
            
            for dep in dependencies:
                if dep not in added_nodes:
                    d2_script += f'{dep} {{\n    style: {{\n        fill: "#45b7d1"\n    }}\n}}\n'
                    added_nodes.add(dep)
                
                d2_script += f'{package} -> {dep}\n'
        
        return d2_script
    
    def visualize_graph(self, graph: Dict[str, List[str]], config: Dict):
        """Визуализация графа и сохранение в PNG"""
        print("\ncleВизуализация графа")
        
        # Генерация D2 скрипта
        d2_script = self.generate_d2_script(graph, config['package_name'])
        
        print("Сгенерированный D2 скрипт:")
        print("=" * 40)
        print(d2_script)
        print("=" * 40)
        
        # Сохраняем D2 скрипт в файл
        d2_file = "dependencies_graph.d2"
        with open(d2_file, 'w', encoding='utf-8') as f:
            f.write(d2_script)
        
        print(f" D2 скрипт сохранен в: {d2_file}")
        
        # Пытаемся сгенерировать PNG, если D2 установлен
        try:
            output_file = config['output_file']
            result = subprocess.run(
                ['d2', d2_file, output_file], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f" Граф сохранен в файл: {output_file}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  Не удалось сгенерировать PNG (D2 не установлен)")
            print(" Установите D2: curl -fsSL https://d2lang.com/install.sh | sh")
        
        # Демонстрация для нескольких пакетов
        self.demo_multiple_packages()
    
    def demo_multiple_packages(self):
        """Демонстрация визуализации для трех различных пакетов"""
        demo_packages = ['flask', 'numpy', 'pandas']
        print(f"\n Примеры визуализации для пакетов: {', '.join(demo_packages)}")
        print("   Запустите инструмент с этими пакетами для сравнения!")
    
    def compare_with_standard_tools(self, package_name: str):
        """Сравнение со штатными инструментами визуализации"""
        print(f"\n Сравнение с штатными инструментами для '{package_name}':")
        print("   Стандартные инструменты Python:")
        print("   - pipdeptree: показывает дерево зависимостей")
        print("   - pip show: базовая информация о пакете")
        print("   - poetry show: если используется Poetry")
        print("\n   Преимущества нашего инструмента:")
        print("   + Визуальное представление в формате PNG")
        print("   + Обнаружение циклических зависимостей")
        print("   + Гибкая настройка через конфигурационный файл")
        print("   + Поддержка тестового режима")

def visualization_stage(graph: Dict[str, List[str]], config: Dict):
    """Этап 5: Визуализация графа"""
    visualizer = GraphVisualizer()
    
    # Визуализация основного графа
    visualizer.visualize_graph(graph, config)
    
    # Сравнение со стандартными инструментами
    visualizer.compare_with_standard_tools(config['package_name'])