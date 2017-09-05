\version "{{ piece.version}}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}
{%- block IDblock %}
{%- endblock %}

#(ly:set-option 'relative-includes #t)
\include "defs.ily"
{%- for item in moreincludes %}
\include "{{ item }}"
{% endfor %}

\header {
  {%- block globalheader %}
  {%- endblock -%}
}

\book {
  {%- block book %}
  {%- endblock %}
  \layout {
    {%- block layout %}
    {%- endblock %}
  }
  \midi {
    {%- block midi %}
    {%- endblock %}
  }
  \paper {
    {%- block paper %}
    {%- endblock %}
  }
}
