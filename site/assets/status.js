(() => {
  const currentPath = window.location.pathname.replace(/^\/+|\/+$/g, '');
  const scenes = {
    '': ['PUBLIC STATUS', 'Company and portfolio', 'A coherent public frame for the estate.'],
    company: ['COMPANY', 'Ownership and purpose', 'The institutional context holds the portfolio.'],
    foundation: ['FOUNDATION', 'Completed foundational work', 'The building-block principle makes further products and tools possible.'],
    reframe: ['PRODUCT', 'Reference implementation', 'The flagship remains a separate product claim.'],
    midi2: ['OPEN INFRASTRUCTURE', 'Normative boundary', 'The MIDI Association remains authoritative.'],
    'product-fields': ['PRODUCT FIELDS', 'Distinct economic objects', 'Products, platforms, and infrastructure stay separate.'],
    'business-architecture': ['STRATEGIC MODEL', 'Capabilities to evidence', 'The company is read as a connected architecture.'],
    'business-model': ['PORTFOLIO', 'Business model boundaries', 'Different economic engines require different models.'],
    evidence: ['EVIDENCE', 'Claim ledger', 'Published statements stay tied to inspectable proof.'],
    transparency: ['TRANSPARENCY', 'Publication boundary', 'Current, proposed, and protected states remain distinct.'],
    ci: ['IDENTITY SYSTEM', 'Readable publication', 'Form gives semantic weight a visible order.'],
    'for-agents': ['MACHINE ENTRY', 'Authority and routes', 'Agents receive the same bounded publication map.']
  };

  const main = document.querySelector('main.screenplay-page');
  const breadcrumbs = main?.querySelector('.breadcrumbs');
  if (main && breadcrumbs && !main.querySelector('.screenplay-plate')) {
    const scene = scenes[currentPath] || scenes[''];
    const plate = document.createElement('figure');
    plate.className = 'screenplay-plate';
    plate.setAttribute('aria-label', `Screenplay scene plate: ${scene[0]}`);
    const caption = document.createElement('figcaption');
    caption.innerHTML = '<strong>SCENE</strong>';
    const synopsis = document.createElement('p');
    synopsis.className = 'plate-synopsis';
    synopsis.textContent = currentPath === 'company'
      ? 'Company profile'
      : currentPath === 'foundation'
        ? 'Technical development foundation'
        : 'Public status record';
    const stage = document.createElement('div');
    stage.className = 'plate-stage';
    const labels = currentPath === 'product-fields'
      ? [scene[0], 'APPLICATIONS']
      : [scene[0], scene[1], scene[2]];
    const sub = currentPath === 'product-fields'
      ? ['section', 'list']
      : currentPath === 'company'
        ? ['company role', 'purpose', 'CLAIM']
        : currentPath === 'foundation'
          ? ['building blocks', 'reuse', 'CLAIM']
          : ['context', 'object', 'CLAIM'];
    labels.forEach((label, index) => {
      const beat = document.createElement('div');
      beat.className = `plate-beat${index === 1 ? ' is-active' : ''}`;
      beat.dataset.index = `0${index + 1}`;
      beat.innerHTML = `<strong>${index === 2 ? `“${label}”` : label}</strong><span>${sub[index]}</span>`;
      stage.appendChild(beat);
    });
    plate.append(caption, synopsis, stage);
    breadcrumbs.after(plate);
  }

  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const updateThemeLabel = () => {
    const active = systemTheme.matches ? 'dark' : 'light';
    document.querySelectorAll('[data-theme-image-dark][data-theme-image-light]').forEach((image) => {
      image.setAttribute('src', active === 'dark' ? image.dataset.themeImageDark : image.dataset.themeImageLight);
    });
  };
  systemTheme.addEventListener?.('change', updateThemeLabel);
  updateThemeLabel();

  const button = document.querySelector('.nav-toggle');
  const rail = document.querySelector('.site-rail');
  if (!button || !rail) return;
  button.addEventListener('click', () => {
    const open = rail.classList.toggle('open');
    button.setAttribute('aria-expanded', String(open));
  });
})();
