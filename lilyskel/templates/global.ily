\version "{{ piece.version }}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}

{{ lyglobal.var_name(movement.num, slash=False) }} = {
{%- if movement.tempo %}
  \tempo "{{ movement.tempo }}"
  {% endif %}
  {%- if movement.time %}
  \time {{ movement.time }}
  {% endif %}
  % INSERT PROPER SPACERS AND BARLINES HERE
  \bar "|."
}

{# vim: se ft=lilypond: #}
