#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de deprecaciones para el Proyecto Final SEM Multi-Agente.
Ejecutar periodicamente para detectar cambios en las APIs antes de que rompan el codigo.

Uso:
    python check_deprecations.py
"""
import sys
import warnings
import importlib
import json
from pathlib import Path

# Capturar DeprecationWarnings
warnings.simplefilter("always", DeprecationWarning)
warnings.simplefilter("always", FutureWarning)
warnings.simplefilter("always", PendingDeprecationWarning)

RESULTS = {"status": "OK", "warnings": [], "errors": [], "versions": {}}


def check_version(package_name, import_name=None):
    """Verifica que un paquete este instalado y reporta su version."""
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


def check_torch_api():
    """Verifica que la API de torchvision para ResNet-18 siga vigente."""
    print("\n--- PyTorch / torchvision ---")
    if not check_version("torch"):
        return
    if not check_version("torchvision"):
        return

    from torchvision import models

    # Verificar que ResNet18_Weights existe
    try:
        weights_cls = models.ResNet18_Weights
        _ = weights_cls.IMAGENET1K_V1
        print("  OK: ResNet18_Weights.IMAGENET1K_V1 existe")
    except AttributeError as e:
        msg = f"ResNet18_Weights.IMAGENET1K_V1 ya no existe: {e}"
        RESULTS["errors"].append(msg)
        print(f"  ERROR: {msg}")

    # Verificar que models.resnet18(weights=...) funciona
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            print("  OK: models.resnet18(weights=...) funciona")
        except Exception as e:
            msg = f"models.resnet18() fallo: {e}"
            RESULTS["errors"].append(msg)
            print(f"  ERROR: {msg}")

        for warning in w:
            msg = f"[torchvision] {warning.category.__name__}: {warning.message}"
            RESULTS["warnings"].append(msg)
            print(f"  WARN: {msg}")


def check_langchain_api():
    """Verifica que las APIs de LangChain usadas en NB04 sigan vigentes."""
    print("\n--- LangChain ---")
    if not check_version("langchain"):
        return
    if not check_version("langchain-core", "langchain_core"):
        return
    if not check_version("langchain-openai", "langchain_openai"):
        return

    # Verificar imports criticos
    critical_imports = [
        ("langchain_openai", "ChatOpenAI"),
        ("langchain_core.tools", "tool"),
        ("langchain_core.prompts", "ChatPromptTemplate"),
        ("langchain_core.prompts", "MessagesPlaceholder"),
        ("langchain_core.messages", "HumanMessage"),
        ("langchain.agents", "create_tool_calling_agent"),
        ("langchain.agents", "AgentExecutor"),
    ]

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        for module_name, attr_name in critical_imports:
            try:
                mod = importlib.import_module(module_name)
                obj = getattr(mod, attr_name)
                print(f"  OK: {module_name}.{attr_name}")
            except (ImportError, AttributeError) as e:
                msg = f"{module_name}.{attr_name} no disponible: {e}"
                RESULTS["errors"].append(msg)
                print(f"  ERROR: {msg}")

        for warning in w:
            msg = f"[langchain] {warning.category.__name__}: {warning.message}"
            RESULTS["warnings"].append(msg)
            print(f"  WARN: {msg}")


def check_langgraph_api():
    """Verifica que las APIs de LangGraph usadas en NB04 sigan vigentes."""
    print("\n--- LangGraph ---")
    if not check_version("langgraph"):
        return

    critical_imports = [
        ("langgraph.graph", "StateGraph"),
        ("langgraph.graph", "START"),
        ("langgraph.graph", "END"),
        ("langgraph.graph.message", "add_messages"),
    ]

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        for module_name, attr_name in critical_imports:
            try:
                mod = importlib.import_module(module_name)
                obj = getattr(mod, attr_name)
                print(f"  OK: {module_name}.{attr_name}")
            except (ImportError, AttributeError) as e:
                msg = f"{module_name}.{attr_name} no disponible: {e}"
                RESULTS["errors"].append(msg)
                print(f"  ERROR: {msg}")

        for warning in w:
            msg = f"[langgraph] {warning.category.__name__}: {warning.message}"
            RESULTS["warnings"].append(msg)
            print(f"  WARN: {msg}")


def check_chromadb_api():
    """Verifica que la API de ChromaDB siga vigente."""
    print("\n--- ChromaDB ---")
    if not check_version("chromadb"):
        return

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            import chromadb
            client = chromadb.EphemeralClient()
            col = client.get_or_create_collection("test_deprecation_check")
            client.delete_collection("test_deprecation_check")
            print("  OK: EphemeralClient + get_or_create_collection funciona")
        except Exception as e:
            msg = f"ChromaDB API cambio: {e}"
            RESULTS["errors"].append(msg)
            print(f"  ERROR: {msg}")

        for warning in w:
            msg = f"[chromadb] {warning.category.__name__}: {warning.message}"
            RESULTS["warnings"].append(msg)
            print(f"  WARN: {msg}")


def main():
    print("=" * 60)
    print("VERIFICACION DE DEPRECACIONES — Proyecto Final SEM")
    print("=" * 60)

    check_version("Python", "sys")
    RESULTS["versions"]["Python"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    check_torch_api()
    check_langchain_api()
    check_langgraph_api()
    check_chromadb_api()

    # Resumen
    print("\n" + "=" * 60)
    n_warn = len(RESULTS["warnings"])
    n_err = len(RESULTS["errors"])

    if n_err > 0:
        RESULTS["status"] = "ERRORS"
        print(f"RESULTADO: {n_err} ERRORES, {n_warn} warnings")
        print("Accion requerida: revisar CONTRIBUTING.md para instrucciones de actualizacion")
    elif n_warn > 0:
        RESULTS["status"] = "WARNINGS"
        print(f"RESULTADO: {n_warn} warnings (posibles deprecaciones futuras)")
        print("Accion recomendada: planear actualizacion antes de la siguiente version")
    else:
        print("RESULTADO: Todo OK. Sin deprecaciones detectadas.")

    # Guardar reporte
    report_path = Path(__file__).parent / "reports" / "deprecation_check.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nReporte guardado: {report_path}")


if __name__ == "__main__":
    main()
