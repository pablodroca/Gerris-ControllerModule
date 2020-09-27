#include <gmodule.h>
#include <stdio.h>

int main (int argc, char * argv[])
{
  return 0;
  //Modules check disabled as Controller initialization are not prepared for discovery and hangs the compilation cycle.
  if (g_module_supported ()) {
    guint i;
    for (i = 1; i < argc; i++) {
      GModule * module = g_module_open (argv[i], 0);
      if (module) {
	gpointer name = NULL;
	if (g_module_symbol (module, "gfs_module_name", &name))
	  printf ("%s\n", (gchar *) name);
	g_module_close (module);
      }
    }
  }
  return 0;
}
