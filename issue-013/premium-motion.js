// Progressive enhancement: all content is visible without this script.
// No scroll listeners, parallax, continuous animation, or rendering dependency.
const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (!preference.matches && 'IntersectionObserver' in window && Element.prototype.animate) {
  const animations = new Set();
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      observer.unobserve(entry.target);
      if (preference.matches) continue;
      const animation = entry.target.animate(
        [{ transform: 'translateY(12px)', opacity: .82 }, { transform: 'translateY(0)', opacity: 1 }],
        { duration: 540, easing: 'cubic-bezier(.2,.7,.3,1)', fill: 'none' }
      );
      animations.add(animation);
      animation.finished.then(() => animations.delete(animation)).catch(() => animations.delete(animation));
    }
  }, { threshold: .08, rootMargin: '0px 0px -24px 0px' });
  document.querySelectorAll('.glance-panel,.ownership-note,.story > section').forEach(element => observer.observe(element));
  preference.addEventListener('change', event => {
    if (!event.matches) return;
    observer.disconnect();
    for (const animation of animations) animation.cancel();
  });
}
