\version "{{ piece.version }}"
{% if piece.language %}
\language "{{ piece.language }}"
{% endif %}
% defs.ily - important information for {{ piece.headers.title }}

\header {
  title = "{{ piece.headers.title }}"
  composer = "{{ piece.headers.composer.name }}"
  {%- if piece.headers.dedication %}
  dedication = "{{ piece.headers.dedication }}"
  {%- endif %}
  {%- if piece.headers.subtitle %}
  subtitle = "{{ piece.headers.subtitle }}"
  {%- endif %}
  {%- if piece.headers.subsubtitle %}
  subsubtitle = "{{ piece.headers.subsubtitle }}"
  {%- endif %}
  {%- if piece.headers.poet %}
  poet = "{{ piece.headers.poet }}"
  {%- endif %}
  {%- if piece.headers.meter %}
  meter = "{{ piece.headers.meter }}"
  {%- endif %}
  {%- if piece.headers.arranger %}
  arranger = "{{ piece.headers.arranger }}"
  {%- endif %}
  {%- if piece.headers.tagline %}
  tagline = "{{ piece.headers.tagline }}"
  {%- endif %}
  {%- if piece.headers.copyright %}
  copyright = "{{ piece.headers.copyright }}"
  {%- endif %}
  {%- if piece.headers.mutopiaheaders %}
  % Mutopia Headers
  instruments = "{{ piece.headers.mutopiaheaders.instruments }}"
  source = "{{ piece.headers.mutopiaheaders.source }}"
  style = "{{ piece.headers.mutopiaheaders.style }}"
  license = "{{ piece.headers.mutopiaheaders.license }}"
  composer = "{{ piece.headers.mutopiaheaders.composer }}"
  maintainer = "{{ piece.headers.mutopiaheaders.maintainer }}"
  {%- if piece.headers.mutopiaheaders.maintainerEmail %}
  maintainerEmail = "{{ piece.headers.mutopiaheaders.maintainerEmail }}"
  {%- endif %}
  {%- if piece.headers.mutopiaheaders.maintainerWeb %}
  maintainerWeb = "{{ piece.headers.mutopiaheaders.maintainerWeb }}"
  {%- endif %}
  {%- if piece.headers.mutopiaheaders.mutopiatitle %}
  mutopiatitle = "{{ piece.headers.mutopiaheaders.mutopiatitle }}"
  {% endif %}
  {%- if piece.headers.mutopiaheaders.mutopiapoet %}
  mutopiapoet = "{{ piece.headers.mutopiaheaders.mutopiapoet }}"
  {%- endif %}
  {%- if piece.headers.mutopiaheaders.mutopiaopus %}
  mutopiaopus = "{{ piece.headers.mutopiaheaders.mutopiaopus }}"
  {% endif %}
  {%- if piece.headers.mutopiaheaders.date %}
  date = "{{ piece.headers.mutopiaheaders.date }}"
  {%- endif %}
  {%- if piece.headers.mutopiaheaders.moreinfo %}
  moreinfo = "{{ piece.headers.mutopiaheaders.moreinfo }}"
  {%- endif %}
  {%- endif %}
}

\include "includes.ily"

{# vim se: tw=1000: #}
