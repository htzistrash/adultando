# Adultando — landing page

Landing page estática de captação de leads. Foco atual: **visual + coleta de e-mail**.

## Rodar

```bash
npm install
npm run dev     # compila o CSS e fica observando alterações
npm run serve   # http://localhost:8080
```

Para gerar o CSS final:

```bash
npm run build
```

O `assets/css/app.css` é versionado de propósito: assim a página abre direto,
sem build, em qualquer hospedagem estática (GitHub Pages, Netlify, Vercel).

## Estrutura

```
index.html              página inteira (uma só)
src/input.css           entrada do Tailwind + paleta + classe .grifo
assets/css/app.css      CSS compilado (gerado — não editar à mão)
assets/img/             imagens
```

## Paleta

Única fonte de cor do projeto. Definida em `src/input.css`, dentro de `@theme`.
Nenhuma cor fora desta lista deve entrar no projeto.

| Token      | Hex       | Uso                                  |
| ---------- | --------- | ------------------------------------ |
| `roxo`     | `#3E1F7A` | fundos escuros, títulos              |
| `uva`      | `#7B3FE4` | marca, botões, CTAs                  |
| `azul`     | `#1E96F0` | apoios, rótulos de seção             |
| `agua`     | `#2BC4B0` | grifos, acentos sobre fundo escuro   |
| `nevoa`    | `#E9EAF0` | fundos alternados, bordas            |
| `grafite`  | `#2D2D2F` | texto corrido, footer                |

Uso em classes Tailwind: `bg-roxo`, `text-uva`, `border-nevoa`, `bg-agua/30` etc.

Notas de contraste, já aplicadas na página:

- `uva` e `roxo` aceitam texto branco.
- `azul` e `agua` **não** têm contraste para texto branco pequeno — só para
  ícones, filetes, bordas e texto escuro por cima.

## Captação de e-mail

Os dois formulários (hero e CTA final) compartilham a classe `.form-lead`.
Hoje eles **não enviam para lugar nenhum**: validam o formato do e-mail,
mostram o estado de sucesso e guardam em `localStorage` (`adultando:leads`)
só para não perder nada durante os testes.

Para ligar de verdade, basta trocar o bloco do `submit` no final do
`index.html` por um `fetch` para o serviço escolhido (Mailchimp, Brevo,
ConvertKit, Formspree ou um endpoint próprio).

## Pendências

- [ ] Conectar os formulários a um provedor de e-mail de verdade
- [ ] Logo definitiva (hoje é um monograma tipográfico)
- [ ] Política de privacidade / aviso de LGPD antes de captar de verdade
- [ ] Domínio + analytics
