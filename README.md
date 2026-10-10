# emv-l3-bitmask-rule-engine 💳🔍

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Showcase-emerald?style=for-the-badge&logo=github)](https://alejano.github.io/emv-l3-bitmask-rule-engine/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![EMVCo](https://img.shields.io/badge/EMVCo-L3%20Certification-orange?style=for-the-badge)](https://emvco.com)

**Autor:** Alejandro Barragán Jasso  
**Enfoque:** Tech Lead / Mobile & Embedded Payment Systems Engineer

> 🌐 **Página Web Interactiva:** Visita las diapositivas interactivas y prueba la calculadora del motor bitmask de 72 bits en [alejano.github.io/emv-l3-bitmask-rule-engine](https://alejano.github.io/emv-l3-bitmask-rule-engine/).

---

## 🎯 Objetivo de la Publicación

Ingeniería inversa en herramientas oficiales de certificación EMV L3 (paquetes `.tpp`, archivos `.tse` y XMLs de reglas).

Descubrimientos clave:
1. **Fórmula Matemática Oficial de 72 Bits:**  
   $$\text{Aplicable} = (\text{ConfiguraciónTerminal} \ \& \ \text{Mask2}) == (\text{Mask1} \ \& \ \text{Mask2})$$
2. **El Hallazgo de CVM:** El motor oficial nunca evalúa Firma ni CDCVM en la máscara; únicamente evalúa Online PIN. Alterando los tags TLV de la tarjeta (Tag 8E), se pueden inyectar pruebas Multi-CVM.
3. **Integridad Criptográfica:** Recálculo estricto de hashes SHA-1 (`<!--BASE64(SHA1(body))-->`) y sumas SHA-256 en `Manifest.json`.

---

## 🚀 Cómo Probar el Código

```bash
python bitmask_rule_engine.py
```

---

## 📱 Publicación en LinkedIn
El texto para LinkedIn y el guión del carrusel están en [POST_LINKEDIN.md](POST_LINKEDIN.md).
