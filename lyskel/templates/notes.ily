\version "{{ piece.version }}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}

{{ instrument.var_name(movement.num, slash=False) }} = \relative {
  {%- if instrument.name == 'global' and movement.tempo %}
  \tempo "{{ movement.tempo }}"
  {%- endif %}
}
