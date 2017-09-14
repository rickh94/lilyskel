\version "{{ piece.version }}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}

% includes.ily - included files for {{ piece.title }}

#(ly:set-option 'relative-includes #t)
{% for item in includepaths %}
\include "{{ item }}"
{% endfor %}
