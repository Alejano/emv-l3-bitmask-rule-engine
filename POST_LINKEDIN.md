# Post 3: Certificación EMV L3: Ingeniería Inversa en Motores Bitmask

**Autor:** Alejandro Barragán Jasso  
**Enfoque:** Tech Lead / Mobile & Embedded Payment Systems Engineer

---

## 📱 Copia para Publicación en LinkedIn

```text
💳 Descifrando la "caja negra": Ingeniería inversa en herramientas oficiales de certificación EMV L3

Durante un proceso de certificación de pagos frente a marcas de tarjetas internacionales, nos encontramos con una limitación crítica: la suite oficial de pruebas no permitía configurar escenarios combinados (multi-CVM) desde su interfaz gráfica.

En lugar de quedarnos bloqueados, analizamos la estructura interna de los archivos de intercambio EMVCo L3tse (paquetes comprimidos con XMLs y firmas de integridad).

Descubrimos que la aplicabilidad de los casos no dependía del nombre de la tarjeta, sino de un motor matemático de bitmasks de 72 bits.

En este carrusel te muestro cómo funciona la fórmula y cómo logramos inyectar casos de prueba personalizados sin corromper el validador oficial. 👇

#EMV #Fintech #ReverseEngineering #PaymentSystems #Testing #Cybersecurity #SoftwareEngineering
```

---

## 📊 Pregunta de Debate

> *"¿Alguna vez tuviste que desarmar una herramienta de certificación o software de terceros para entender por qué rechazaba tus pruebas?"*

---

## 📐 Fórmula de Aplicabilidad

$$\text{Aplicable} = (\text{ConfiguraciónTerminal} \ \& \ \text{Mask2}) == (\text{Mask1} \ \& \ \text{Mask2})$$

---

## 💻 Código de Ejemplo
El motor ejecutable completo se encuentra en:  
[`examples/03_emv_l3_bitmasks/bitmask_rule_engine.py`](../examples/03_emv_l3_bitmasks/bitmask_rule_engine.py)
