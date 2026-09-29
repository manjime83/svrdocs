# Formato de llamada: fuente del PDF

Fuente del PDF publicado en `docs/ventas/formato-llamada-comprador.pdf`.

- `formato-llamada-comprador.html`: la hoja (una página Letter, blanco y negro, pensada para imprimir).
- `fonts/`: Outfit (títulos) y DM Sans (cuerpo), en TTF. Ambas con licencia SIL OFL.

## Regenerar el PDF

Con Google Chrome instalado (macOS), desde esta carpeta:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=3000 --print-to-pdf=formato-llamada-comprador.pdf file://$PWD/formato-llamada-comprador.html
```

Luego copia el PDF a `docs/ventas/formato-llamada-comprador.pdf`. Verifica que siga siendo una sola página.
