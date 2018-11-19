\version "{{ piece.version}}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}
{%- block IDblock %}
{%- endblock %}

#(ly:set-option 'relative-includes #t)
\include "defs.ily"

\header {
  {%- block globalheader %}
  {%- endblock -%}
}

\book {
  {%- block book %}
  {%- endblock %}
  \paper {
    {%- block paper %}
    {%- endblock %}
  }
}

{# vim: se ft=lilypond :#}
