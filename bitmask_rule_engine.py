"""
bitmask_rule_engine.py
Motor de Reglas Bitmask de 72 Bits e Inyector de Pruebas EMV L3 (Pharos / L3tse)
Autor: Alejandro Barragán Jasso
Tema 3: Certificación EMV L3: Ingeniería Inversa en Motores de Reglas Bitmask

Fórmula descubierta:
  Aplicable = (ConfiguraciónTerminal & Mask2) == (Mask1 & Mask2)
  Donde:
  - Mask2: "Care Mask" (bits relevantes evaluados)
  - Mask1: "Expected Value" (valor requerido para dichos bits)
"""

import hashlib
import base64
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Tuple, List

class EmvBitmaskEngine:
    """Motor de evaluación de aplicabilidad de pruebas de certificación EMV L3."""

    # 72 bits = 9 bytes (18 caracteres hexadecimales)
    BITMASK_HEX_LEN = 18

    # Significado de bits clave en la arquitectura de terminal EMV Contactless / Contact
    BIT_DEFINITIONS = {
        0: "Soporte de Contacto (Chip EMV)",
        1: "Soporte de Contactless (NFC)",
        2: "Soporte de Banda Magnética (Magstripe)",
        8: "Soporte de Online PIN",
        9: "Soporte de Firma Manuscrita (Signature)",
        10: "Soporte de Sin CVM (No CVM)",
        11: "Soporte de CDCVM (Mobile Wallet / Apple Pay / Google Pay)",
        24: "Modo Offline Data Authentication (ODA - SDA/DDA/CDA)",
        32: "Terminal Desatendida (Kiosko/Vending)",
        48: "Soporte de Moneda Nacional / Multi-Divisa"
    }

    @staticmethod
    def parse_hex_mask(mask_hex: str) -> int:
        """Convierte un string hexadecimal de hasta 72 bits en un entero de Python."""
        clean_hex = mask_hex.strip().replace("0x", "").zfill(18)
        return int(clean_hex, 16)

    @staticmethod
    def format_mask_hex(mask_val: int) -> str:
        """Formatea un entero a representación hexadecimal de 18 caracteres (72 bits)."""
        return f"{mask_val:018X}"

    @classmethod
    def evaluate_rule(cls, terminal_config_hex: str, mask1_hex: str, mask2_hex: str) -> Tuple[bool, str]:
        """
        Aplica la fórmula matemática oficial:
        (Terminal & Mask2) == (Mask1 & Mask2)
        """
        term = cls.parse_hex_mask(terminal_config_hex)
        m1 = cls.parse_hex_mask(mask1_hex)
        m2 = cls.parse_hex_mask(mask2_hex)

        actual_evaluated = term & m2
        expected_evaluated = m1 & m2
        is_applicable = (actual_evaluated == expected_evaluated)

        explanation = (
            f"Terminal: {cls.format_mask_hex(term)}\n"
            f"CareMask: {cls.format_mask_hex(m2)}\n"
            f"Expected: {cls.format_mask_hex(m1)}\n"
            f"Actual & Care   = {cls.format_mask_hex(actual_evaluated)}\n"
            f"Expected & Care = {cls.format_mask_hex(expected_evaluated)}\n"
            f"Resultado: {'APLICABLE (Pasa filtro)' if is_applicable else 'NO APLICABLE (Descartado)'}"
        )
        return is_applicable, explanation


class L3TestInjector:
    """Inyector de casos de prueba personalizados en estructuras XML de EMVCo."""

    @staticmethod
    def calculate_xml_integrity_signature(xml_content: str) -> str:
        """
        Calcula la firma de integridad que el validador oficial exige al final del XML:
        <!--BASE64(SHA1(body + "\\n"))-->
        """
        payload = (xml_content.strip() + "\n").encode("utf-8")
        sha1_digest = hashlib.sha1(payload).digest()
        b64_sig = base64.b64encode(sha1_digest).decode("ascii")
        return f"<!--{b64_sig}-->"

    @staticmethod
    def calculate_manifest_checksum(file_bytes: bytes) -> str:
        """Calcula el checksum SHA-256 requerido por Manifest.json y ProjectInfo.json."""
        return hashlib.sha256(file_bytes).hexdigest().upper()

    @classmethod
    def build_custom_test_case_xml(
        cls,
        test_id: str,
        test_name: str,
        mask1_hex: str,
        mask2_hex: str,
        tlv_cvm_list: str = "000000000000000002010100", # Online PIN + Signature + No CVM
        tlv_aid: str = "A0000000031010"
    ) -> str:
        """Genera un nodo <Test> firmado para RuleSet.xml."""
        body = f"""<Test ID="{test_id}" Name="{test_name}">
    <Bitmask Rule="Applicability">
        <Mask1>{mask1_hex}</Mask1>
        <Mask2>{mask2_hex}</Mask2>
    </Bitmask>
    <CardProfile>
        <AID>{tlv_aid}</AID>
        <Tag8E_CVMList>{tlv_cvm_list}</Tag8E_CVMList>
        <Behavior Mode="Multi-CVM-Forced"/>
    </CardProfile>
</Test>"""
        signature = cls.calculate_xml_integrity_signature(body)
        return f"{body}\n{signature}"


def run_demo():
    print("=" * 70)
    print("DEMOSTRACIÓN: INGENIERÍA INVERSA EN CERTIFICACIÓN EMV L3")
    print("Autor: Alejandro Barragán Jasso")
    print("=" * 70)

    # Simular una terminal POS Contactless con Online PIN y Firma
    # Bits activos: Contactless (bit 1) + Online PIN (bit 8) + Signature (bit 9)
    # (1 << 1) | (1 << 8) | (1 << 9) = 2 | 256 | 512 = 770 = 0x0000000000000302
    terminal_caps = "000000000000000302"

    print("\n1. Evaluando Regla Estándar de Visa Contactless:")
    # Regla: Exige Contactless (bit 1) y Online PIN (bit 8).
    # Mask2 (Care): evalúa bits 1 y 8 (0x000000000000000102)
    # Mask1 (Expected): exige que ambos estén en 1 (0x000000000000000102)
    mask1 = "000000000000000102"
    mask2 = "000000000000000102"

    applicable, debug_info = EmvBitmaskEngine.evaluate_rule(terminal_caps, mask1, mask2)
    print(debug_info)

    print("\n2. Evaluando Caso de Terminal Desatendida (Kiosko - Bit 32):")
    # Mask2 exige evaluar bit 32 (0x000000010000000000)
    # Mask1 exige que esté activo
    mask1_kiosk = "000000010000000000"
    mask2_kiosk = "000000010000000000"
    applicable_kiosk, debug_kiosk = EmvBitmaskEngine.evaluate_rule(terminal_caps, mask1_kiosk, mask2_kiosk)
    print(debug_kiosk)

    print("\n3. Inyectando Caso Multi-CVM con Hash de Integridad SHA-1:")
    custom_xml = L3TestInjector.build_custom_test_case_xml(
        test_id="CUSTOM_MC_099",
        test_name="Contactless Multi-CVM Fallback Simulation",
        mask1_hex=mask1,
        mask2_hex=mask2,
        tlv_cvm_list="000000000000000002010100"
    )
    print("XML Generado con Firma Válida:")
    print("-" * 50)
    print(custom_xml)
    print("-" * 50)

    sha256_chk = L3TestInjector.calculate_manifest_checksum(custom_xml.encode("utf-8"))
    print(f"Checksum SHA-256 para Manifest.json: {sha256_chk}")
    print("\n Demostración de Tema 3 finalizada con éxito.")


if __name__ == "__main__":
    run_demo()
