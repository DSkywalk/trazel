/*----------------------------------------------------------------------------*/
/*--  mte.c                                                                 --*/
/*--  MTE Search Tool                                                       --*/
/*--  Copyright (C) 2013 CUE                                                --*/
/*--                                                                        --*/
/*--  This program is free software: you can redistribute it and/or modify  --*/
/*--  it under the terms of the GNU General Public License as published by  --*/
/*--  the Free Software Foundation, either version 3 of the License, or     --*/
/*--  (at your option) any later version.                                   --*/
/*--                                                                        --*/
/*--  This program is distributed in the hope that it will be useful,       --*/
/*--  but WITHOUT ANY WARRANTY; without even the implied warranty of        --*/
/*--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          --*/
/*--  GNU General Public License for more details.                          --*/
/*--                                                                        --*/
/*--  You should have received a copy of the GNU General Public License     --*/
/*--  along with this program. If not, see <http://www.gnu.org/licenses/>.  --*/
/*----------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <sys/stat.h>

/*----------------------------------------------------------------------------*/
#define _MTE_VERBOSE_
#define _MTE_SAVE_INFO_

#define BYTE_256 0x00000100
#define KILO_16  0x00004000
#define MEGA_16  0x01000000


/*----------------------------------------------------------------------------*/
char *textname, *rulename, *outname;
int   codesize, minsize, maxsize, number, control, total;

unsigned char  id[256][2];
unsigned int   id_total;

/*----------------------------------------------------------------------------*/
void  Title(void);
void  Usage(void);
void  MTE(void);
char *LoadRules(char *filename);
int   FileSize(char *filename);
void *FileLoad(char *filename);
void  FileSave(char *filename, void *buffer, int length);
void  Folder(char *path);
void *Allocate(int length, int size);
void *ReAllocate(void *buffer, int length, int size);
void  Free(void *buffer);
void  Exit(const char *format, ...);

/*----------------------------------------------------------------------------*/
int main(int argc, char **argv) {
  Title();
  if (argc != 10) Usage();

  textname = argv[1];
  rulename = argv[2];
  codesize = strtol(argv[3], NULL, 0);
  minsize  = strtol(argv[4], NULL, 0);
  maxsize  = strtol(argv[5], NULL, 0);
  number   = strtol(argv[6], NULL, 0);
  control  = strtol(argv[7], NULL, 0);
  total    = strtol(argv[8], NULL, 0);
  outname  = argv[9];

  MTE();

  printf("Done\n");

  exit(EXIT_SUCCESS);
}

/*----------------------------------------------------------------------------*/
void Title(void) {
  printf(
    "\n"
    "MTE Search Tool v1.1\n"
    "Copyright (C) 2013 CUE\n"
    "\n"
  );
}

/*----------------------------------------------------------------------------*/
void Usage(void) {
  Exit(
    "Usage: MTE filename rules codesize minsize maxsize number total output\n"
    "\n"
    "filename ... text file to analyze\n"
    "rules ...... rules table file\n"
    "codesize ... MTE code size\n"
    "minsize .... minimum MTE string length\n"
    "maxsize .... maximum MTE string length\n"
    "number ..... minimum number of occurrences\n"
    "control .... add the MTE size in the operations (0/1)\n"
    "total ...... number of MTE to search\n"
    "output ..... output file name\n"
  );
}

/*----------------------------------------------------------------------------*/
void MTE(void) {
  unsigned char  *text, *rules, *output, *src, *tgt, *end, txt[256];
  unsigned char **stack, **stk, **stk_end, **b_stack;
  unsigned int    length, add, index, idx, best, count, size, total_saved;
  unsigned int    b_count, b_size, b_save, total_mte;
  unsigned int    i, j, t;

  // controles
  if (total < 1) Exit("The total of MTE must be a valid value\n");
  if (control && (control != 1)) Exit("Bad control value\n");
  if (minsize < 2) Exit("Minimum must be 2 or greater\n");
  if (minsize > maxsize) Exit("Minimum can not be greater as maximum\n");

  // crea la tabla de reglas
  rules = LoadRules(rulename);

  // lee el fichero a analizar
  length = FileSize(textname);
  if (length >= MEGA_16) Exit("File too big\n");
  text = FileLoad(textname);


  // elimina texto entre códigos
  for (t = 0; t < id_total; t++) {
    for (i = 0; i < length; i++) {
      if (text[i] == id[t][0]) {
        for (j = i; j < length; j++) {
          if (text[j] == id[t][1]) break;
          text[j] = 0;
        }
        if (j < length) text[j] = 0;
        i = j;
      }
    }
  }

  // simplifica los caracteres no permitidos
  for (i = 0; i < length; i++) if (!rules[text[i]]) text[i] = 0;

  // crea la tabla de MTE encontrados
  index  = KILO_16;
  output = Allocate(index, sizeof(char));
  idx    = 0;

#ifdef _MTE_SAVE_INFO_
  j = sprintf(txt, "%s", "MTE Search Tool - Copyright (C) 2013 CUE\r\n\r\n");
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "filename ..... %s\r\n", textname);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "rules ........ %s\r\n", rulename);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "codesize ..... %d\r\n", codesize);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "minimum ...... %d\r\n", minsize);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "maximum ...... %d\r\n", maxsize);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "ocurrences ... %d\r\n", number);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "control ...... %d\r\n", control);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
  j = sprintf(txt, "total ........ %d\r\n\r\n", total);
  for (i = 0; i < j; i++) output[idx++] = txt[i];
#endif

  // total de espacio ahorrado sin contar el usado por los MTE
  total_saved = 0;

  // espacio ocupado por los MTE
  total_mte = 0;

  // bucle de búsqueda de MTE
  for (t = 0; t < total; t++) {

    // reduce los datos anulando separaciones innecesarias
    for (i = length, src = text, tgt = NULL; i--; src++) {
      if (!*src) {
        if ((tgt != NULL) && (src - tgt < minsize)) {
          while (tgt < src) *tgt++ = 0;
        }
        tgt = src;
      }
    }

    // reduce los datos eliminando caracteres no permitidos innecesarios
    for (add = 0, src = tgt = text; length--; src++) {
      if (*src) {
        *tgt++ = *src;
        add = 1;
      } else if (add) {
        *tgt++ = 0;
        add = 0;
      }
    }
    length = tgt - text;

    // inicializa los datos del mejor MTE
    b_stack = NULL;
    b_count = 0;
    b_size  = 0;
    b_save  = 0;
    best    = 1;

    // bucle para cada longitud deseada
    for (size = minsize; size <= maxsize; size++) {

      // comprueba que la longitud sea válida
      if (size > length) break;
      if (size <= codesize) { continue; }

      // busca para cada posible MTE
      end = text + length - size;
      for (src = text; src <= end; src++) {

        // comprueba que el MTE contenga caracteres permitidos
        if (!*src) continue; // speed up
        if (!*(src + 1)) continue; // speed up
        for (i = 2; i < size; i++) {
          if (!src[i]) {
            src += i;
            break;
          }
        }
        if (i != size) continue;

        // crea la tabla de posiciones de cada aparición del MTE
        if (best) { // speed up
          stack = Allocate(length / size, sizeof(char *));
          best = 0;
        }

        // añade el primer MTE
        stk = stack;
        *stk++ = src;

        // busca cada aparición del MTE
        for (tgt = src + size; tgt <= end; ) {
          if (*src - *tgt) { tgt++; continue; } // speed up
          if (*(src + 1) - *(tgt + 1)) { tgt++; continue; } // speed up
          for (i = 2; i < size; i++) if (src[i] - tgt[i]) break;
          if (i == size) {
            *stk++ = tgt;
            tgt += size;
          } else {
            tgt++;
          }
        }

        // comprueba el ahorro de bytes
        count = stk - stack;

        if (count >= number) {
          if (count * (size - codesize) >= control * size + b_save) {
            if (b_count) Free(b_stack);
            b_stack = stack;
            b_count = count;
            b_size  = size;
            b_save  = count * (size - codesize) - control * size;

            best = 1;

#ifdef _MTE_VERBOSE_
            printf("\r");
            printf("MTE=%4d, ", t + 1);
            printf("s=%3d, n=%6d, save=%6d, ", b_size, b_count, b_save);
            printf("[");
            j = b_size < 37 ? b_size : 37;
            tgt = b_stack[0];
            for (i = 0; i < j; i++) printf("%c", tgt[i]);
            printf(b_size < 37 ? "]" : "}");
#endif
          }
        }
      }
    }

#ifdef _MTE_VERBOSE_
    if (!b_count) {
      j = size < 50 ? size : 50;
      printf("MTE=%4d, none found, exiting", t + 1);
      for (i = 0; i <= j; i++) printf(" ");
    }
    printf("\n");
#endif

    // borra la tabla usada si no se ha usado
    if (!best) Free(stack);

    // finaliza si no se encontró nada
    if (!b_count) break;

    // mejor MTE encontrado
    src = b_stack[0];

    // comprueba que haya al menos 256B libres en la tabla de MTE
    while (idx + size + BYTE_256 >= index) {
      index += KILO_16;
      output = ReAllocate(output, index, sizeof(char));
    }

    // añade el MTE a la tabla de MTE
#ifdef _MTE_SAVE_INFO_
    j = sprintf(txt, "MTE=%4d, ", t + 1);
    for (i = 0; i < j; i++) output[idx++] = txt[i];
    j = sprintf(txt, "s=%3d, n=%6d, save=%6d, ", b_size, b_count, b_save);
    for (i = 0; i < j; i++) output[idx++] = txt[i];

    total_mte += b_size;
#endif

    output[idx++] = '[';
    for (i = 0; i < b_size; i++) output[idx++] = *src++;
    output[idx++] = ']';
    output[idx++] = '\r';
    output[idx++] = '\n';

    // elimina cada aparición del MTE en los datos iniciales
    stk     = b_stack;
    stk_end = b_stack + b_count;
    while (stk < stk_end) {
      src = *stk++;
      end = src + b_size;
      while (src < end) *src++ = 0;
    }

    // libera la tabla de posiciones
    Free(b_stack);

    // actualiza el total ahorrado
    total_saved += b_save;
  }

#ifdef _MTE_VERBOSE_
  printf("\n");
  i = total_saved + control * total_mte;
  printf("total bytes saved = %d\r\n", i);
  printf("total MTE space   = %d\r\n", total_mte);
  printf("\r\n");
#endif

#ifdef _MTE_SAVE_INFO_
  i = total_saved + control * total_mte;
  j = sprintf(txt, "\r\ntotal bytes saved = %d\r\n", i);
  for (i = 0; i < j; i++) output[idx++] = txt[i];

  j = sprintf(txt, "total MTE space   = %d\r\n", total_mte);
  for (i = 0; i < j; i++) output[idx++] = txt[i];

  j = sprintf(txt, "\r\nend of file\r\n");
  for (i = 0; i < j; i++) output[idx++] = txt[i];
#endif

  // graba la tabla de MTE
  FileSave(outname, output, idx);

  // libera la memoria usada
  Free(output);
  Free(text);
  Free(rules);
}

/*----------------------------------------------------------------------------*/
char *LoadRules(char *filename) {
  unsigned char *buffer, *rules, *tbl, *end;
  unsigned int   length, line, code, ch;
  unsigned int   i;

  length = FileSize(filename);
  if (length >= MEGA_16) Exit("Rules file too big\n");
  buffer = FileLoad(filename);

  rules = Allocate(256, sizeof(char));

  id_total = 0;

  rules[0] = 0;
  for (i = 1; i < 256; i++) rules[i] = 1;

  tbl = buffer;
  end = buffer + length - 1;

  for (line = 1; tbl < end; ) {
    if ((*tbl == ' ') || (*tbl == '\t')) {
      for(tbl++; tbl <= end; tbl++) {
        if ((*tbl != ' ') && (*tbl != '\n')) break;
      }
    } else if (*tbl == '\n') {
      line++;
      tbl++;
    } else if (*tbl == '\r') {
      line++;
      tbl++;
      if (tbl > end) break;
      if (*tbl != '\n') Exit("Expected LF not found in line %d\n", line);
      tbl++;
    } else if (*tbl == ';') {
      for(tbl++; tbl <= end; tbl++) {
        if ((*tbl == '\r') || (*tbl == '\n')) break;
      }
      continue;
    } else if (*tbl == '.') {
      for(tbl++; tbl <= end; tbl++) {
        code = *tbl;
        if ((code == '\r') || (code == '\n')) break;
        rules[code] = 0;
      }
    } else if (*tbl == '-') {
      if (id_total > 255) Exit("Too many ID in line %d\n", line);
      tbl++;
      if (tbl > end) Exit("Expected START_ID not found in line %d\n", line);
      id[id_total][0] = *tbl;
      tbl++;
      if (tbl > end) Exit("Expected END_ID not found in line %d\n", line);
      id[id_total][1] = *tbl;
      tbl++;
      if (tbl > end) break;
      ch = *tbl;
      if ((ch != '\r') && (ch != '\n')) {
        if ((ch != ' ') && (ch != '\t') && (ch != ';')) {
          Exit("Bad ID in line %d\n", line);
        }
      }
      id_total++;
    } else {
      code = 0;
      for (i = 0; i < 2; i++) {
        if (tbl > end) Exit("Bad hexadecimal code in line %d\n", line);
        ch = *tbl++;
        if      ((ch >= '0') && (ch <= '9')) ch -= 48;
        else if ((ch >= 'A') && (ch <= 'F')) ch -= 55;
        else if ((ch >= 'a') && (ch <= 'f')) ch -= 87;
        else Exit("Bad hexadecimal code in line %d\n", line);
        code = (code << 4) | ch;
      }
      rules[code] = 0;
      if (tbl > end) break;
      ch = *tbl;
      if ((ch != '\r') && (ch != '\n')) {
        if ((ch != ' ') && (ch != '\t') && (ch != ';')) {
          Exit("Bad hexadecimal code in line %d\n", line);
        }
      }
    }
  }

  return(rules);
}

/*----------------------------------------------------------------------------*/
int FileSize(char *filename) {
  FILE *fp;
  int   fs;

  if ((fp = fopen(filename, "rb")) == NULL) Exit("File open error\n");
  fseek(fp, 0, SEEK_END); // seek to end of file
  fs = ftell(fp);
  fseek(fp,0, SEEK_SET);
  if (fclose(fp) == EOF) Exit("File close error\n");

  return(fs);
}

/*----------------------------------------------------------------------------*/
void *FileLoad(char *filename) {
  FILE *fp;
  char *fb;
  int   fs;

  if ((fp = fopen(filename, "rb")) == NULL) Exit("File open error\n");
  fseek(fp, 0, SEEK_END); // seek to end of file
  fs = ftell(fp);
  fseek(fp,0, SEEK_SET);
  fb = Allocate(fs, sizeof(char));
  if (fread(fb, 1, fs, fp) != fs) Exit("File read error\n");
  if (fclose(fp) == EOF) Exit("File close error\n");

  return(fb);
}

/*----------------------------------------------------------------------------*/
void FileSave(char *filename, void *fb, int fs) {
  FILE *fp;

  Folder(filename);

  if ((fp = fopen(filename, "w+b")) == NULL) Exit("File create error\n");
  if (fwrite(fb, 1, fs, fp) != fs) Exit("File write error\n");
  if (fclose(fp) == EOF) Exit("File close error\n");
}

/*----------------------------------------------------------------------------*/
void Folder(char *path) {
  int i;

  for (i = 0; path[i]; i++) {
    if ((path[i] == '/') || (path[i] == '\\')) {
      path[i] = 0;
      if (mkdir(path, S_IRWXU|S_IRGRP|S_IXGRP) > 0) Exit("Make directory error\n");
      path[i] = '/';
    }
  }
}

/*----------------------------------------------------------------------------*/
void *Allocate(int length, int size) {
  char *fb;

  fb = (char *)malloc(length * size);
  if (fb == NULL) Exit("Allocate memory error\n");

  return(fb);
}

/*----------------------------------------------------------------------------*/
void *ReAllocate(void *buffer, int length, int size) {
  char *fb;

  fb = realloc(buffer, length * size);
  if (fb == NULL) Exit("Reallocate memory error\n");

  return(fb);
}

/*----------------------------------------------------------------------------*/
void Free(void *buffer) {
  free(buffer);
}

/*----------------------------------------------------------------------------*/
void Exit(const char *format, ...) {
  va_list args;
  
  va_start(args, format);
  vfprintf(stdout, format, args);
  va_end(args);
  
  exit(EXIT_FAILURE);
}

/*----------------------------------------------------------------------------*/
/*--  EOF                                           Copyright (C) 2013 CUE  --*/
/*----------------------------------------------------------------------------*/
