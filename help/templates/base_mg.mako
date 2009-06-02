<%inherit file="/base_help.mako"/>
${next.body()}

<%def name="menu()"><%
self.menuitem('intro.htm', 'Introduction', 'Introduction to musicGuru')
self.menuitem('howto/index.htm', 'How To', 'Quickly get into the action')
self.menuitem('build.htm', 'Build', 'Building your musicGuru collection')
self.menuitem('design.htm', 'Design', 'Designing your to-be collection')
self.menuitem('materialize.htm', 'Materialize', 'Materializing your design')
self.menuitem('naming_models.htm', 'Naming Models', 'How to design your own custom models')
self.menuitem('faq.htm', 'F.A.Q.', 'Frequently Asked Questions')
self.menuitem('versions.htm', 'Version History', 'Changes musicGuru went through')
self.menuitem('credits.htm', 'Credits', 'People who contributed to musicGuru')
%></%def>