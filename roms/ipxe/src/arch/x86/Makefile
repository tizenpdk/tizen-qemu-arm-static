# Include common x86 headers
#
INCDIRS		+= arch/x86/include

# x86-specific directories containing source files
#
SRCDIRS		+= arch/x86/core
SRCDIRS		+= arch/x86/interface/efi
SRCDIRS		+= arch/x86/prefix
SRCDIRS		+= arch/x86/hci/commands

# breaks building some of the linux-related objects
CFLAGS		+= -Ulinux

# disable valgrind
CFLAGS		+= -DNVALGRIND
