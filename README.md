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
index.html                 página inteira (uma só)
src/input.css              entrada do Tailwind: paleta e efeitos
assets/css/app.css         CSS compilado (gerado, não editar à mão)
assets/img/                imagens
scripts/build-artifact.py  gera a versão hospedada no claude.ai
dist/                      saída do script (fora do versionamento)
```

## Prévia hospedada no claude.ai

Para mandar a página para alguém antes de ter domínio, dá para publicá-la
como página hospedada no claude.ai. Ela não aceita o `index.html` como
está: a plataforma injeta o próprio `<!doctype html>`, `<head>` e `<body>`,
e não serve os `.css` relativos.

```bash
npm run build:artifact
```

O script monta `dist/artifact/` a partir do mesmo `index.html`: tira o
invólucro, embute o CSS compilado e copia as imagens. Não existe uma
segunda cópia da página para sair do ar de sincronia. Para publicar, use
`dist/artifact/page.html` como página e os arquivos de
`dist/artifact/assets/` como anexos.

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

Os dois formulários (hero e CTA final) compartilham a classe `.form-lead` e
um único ponto de configuração, no `<script>` do fim do `index.html`:

```js
var CAPTURA = {
  provedor: 'kit',   // 'kit' ou 'formspree'
  id: ''             // vazio = ainda não conectado
};
```

Com `id` vazio o formulário funciona normalmente, mas só guarda os e-mails
em `localStorage` (`adultando:leads`) e avisa no console. Assim a página
continua demonstrável sem depender de conta em lugar nenhum.

### Ligar no Kit (recomendado)

Grátis até 10.000 inscritos, com envios ilimitados. O plano gratuito dá um
formulário, que é exatamente o que a lista de espera precisa.

1. Crie a conta em [kit.com](https://kit.com).
2. **Grow > Landing Pages & Forms > New > Form > Inline**.
3. Abra o formulário criado e olhe a URL:
   `app.kit.com/forms/1234567/edit`. O número é o seu id.
4. Preencha no `index.html`: `provedor: 'kit'`, `id: '1234567'`.
5. Em **Settings > Incentive**, ligue o double opt-in. Além de limpar
   e-mail errado, deixa o consentimento registrado, o que ajuda na LGPD.

Os inscritos aparecem em **Subscribers**, com export em CSV.

### Ligar no Formspree

Mais simples, mas só recebe: não envia campanha e o plano gratuito para em
50 envios por mês, sem export em CSV. Serve se você só quer o e-mail
chegando na sua caixa por enquanto.

1. Crie o form em [formspree.io](https://formspree.io).
2. Copie o endpoint: `https://formspree.io/f/abcdwxyz`.
3. Preencha: `provedor: 'formspree'`, `id: 'abcdwxyz'`.

### Outro provedor

`envia()` isola a chamada. Para Brevo, Mailchimp ou endpoint próprio, é
adicionar um ramo ali com a URL e o formato de payload do serviço.

## Pendências

- [ ] Preencher `CAPTURA.id` com o formulário do provedor escolhido
- [ ] Trocar o relato placeholder (texto e foto) por um depoimento real
- [ ] Página de política de privacidade, linkada no rodapé
- [ ] Domínio + analytics
