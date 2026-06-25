#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de deprecaciones para la Unidad 5 (Sistemas Multi-Agente).
Ejecutar periodicamente para detectar cambios en las APIs antes de que rompan el codigo.

Uso:
    python check_deprecations.py
"""
import sys
import warnings
import importlib
import json

warnings.simplefilter("always", DeprecationWarning)
warnings.simplefilter("always", FutureWarning)

RESULTS = {"status": "OK", "warnings": [], "errors": [], "versions": {}}

def check_version(package_name, import_name=None):
    imp = import_name or package_name
    try:
        mod = importlib.import_module(imp)
        version = getattr(mod, "__version__", "unknown")
        RESULTS["versions"][package_name] = version
        print(f"  OK: {package_name} == {version}")
        return True
    except ImportError:
        RESULTS["errors"].append(f"{package_name} no esta instalado")
        print(f"  ERROR: {package_name} no esta instalado")
        return False

def check_langgraph_api():
    print("\n--- LangGraph ---")
    if not check_version("langgraph"): return
    critical_imports = [("langgraph.graph", "StateGraph"), ("langgraph.graph", "START")]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        for module_name, attr_name in critical_imports:
            try:
                mod = importlib.import_module(module_name)
                getattr(mod, attr_name)
                print(f"  OK: {module_name}.{attr_name}")
            except (ImportError, AttributeError) as e:
                RESULTS["errors"].append(f"{module_name}.{attr_name}: {e}")
                print(f"  ERROR: {module_name}.{attr_name} falló")

def check_crewai_api():
    print("\n--- CrewAI ---")
    if not check_version("crewai"): return
    critical_imports = [("crewai", "Agent"), ("crewai", "Task"), ("crewai", "Crew")]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        for module_name, attr_name in critical_imports:
            try:
                mod = importlib.import_module(module_name)
                getattr(mod, attr_name)
                print(f"  OK: {module_name}.{attr_name}")
            except (ImportError, AttributeError) as e:
                RESULTS["errors"].append(f"{module_name}.{attr_name}: {e}")
                print(f"  ERROR: {module_name}.{attr_name} falló")

def main():
    print("=" * 60)
    print("VERIFICACION DE DEPRECACIONES — UNIDAD 5")
    print("=" * 60)
    check_version("langchain")
    check_version("chromadb")
    check_langgraph_api()
    check_crewai_api()
    
    n_err = len(RESULTS["errors"])
    if n_err > 0:
        print(f"\nRESULTADO: {n_err} ERRORES DETECTADOS. Requiere revisión.")
    else:
        print("\nRESULTADO: Todo OK. Sin deprecaciones críticas detectadas.")

if __name__ == "__main__":
    main()
