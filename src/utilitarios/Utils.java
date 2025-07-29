package utilitarios; 
import java.io.*;

/**
 * Clase Utils
 * Esta clase contiene métodos utilizarios para la lectura de datos básicos
 * y la selección de un valor en un listado de opciones.
 * Entre las opciones de validación de las entradas para facilitar la
 * escritura de códigos sencillos que utilizan "consola".
 * Algunas de las funciones comentarias presentes está la opción de cambiar
 * el color de las fuentes en la consola.
 * 
 * Los listados de colores para la terminal fueron obtenidos del siguiente
 * sitio
 * https://stackoverflow.com/questions/5762491/how-to-print-color-in-console-using-system-out-println
 * 
 * @author Mauricio Andrés Zamora Hernández
 * @version 1.1
 */
public class Utils {
    static BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    static PrintStream out = System.out;

    /**
     * Este método genera un "menú" con las opciones en un arreglo de String.
     * El método coloca automáticamene el número de selección iniciando en 1.
     * Además, este método tiene validaciones para que solo se pueda seleccionar
     * valores válidos y controla excepciones por tipo de entrada incorrecto.
     * 
     * @param etiqueta Texto que se coloca antes de la impresión del menú.
     *                 Se recomienda un texto que indique que significa las
     *                 opciones.
     * @param opciones Las opciones a mostrar.
     * @return El número seleccionado por el usuario del menú mostrado.
     */
    public static int seleccionarElementoTexto(String etiqueta, String[] opciones) {
        int resultado = 0;
        out.println(etiqueta);

        for (int i = 0; i < opciones.length; i++) {
            out.printf("%3d - %s\n", (i + 1), opciones[i]);
        }

        resultado = leerRangosEnteros("Seleccione el ID de la opción", 1, opciones.length);

        return resultado;
    }

    public static int seleccionarElementoEntero(String etiqueta, int[] opciones) {
        int resultado = 0;
        out.println(etiqueta);

        for (int i = 0; i < opciones.length; i++) {
            out.printf("%3d - %d\n", (i + 1), opciones[i]);
        }

        resultado = leerRangosEnteros("Seleccione el ID de la opción", 1, opciones.length);

        return resultado;
    }

    /**
     * Este método permite la lectura de un número entero. Si el usuario digita algo
     * que genere un
     * error, el sistema contniuará solicitando el valor correcto.
     * 
     * @param texto Es el texto utilizado como etiqueta para que el usuario sepa que
     *              se le solicita.
     *              Si no desea imprimir una etiqueta, coloque "".
     * @return Número entero digitado por el usuario.
     */
    public static int leerEntero(String texto) {
        int resultado = 0;
        out.print(texto);

        boolean ocurrioUnaBronca = false;

        do {
            try {
                resultado = Integer.parseInt(in.readLine());
                ocurrioUnaBronca = false;
            } catch (Exception e) {
                ocurrioUnaBronca = true;
                out.println("Intente de nuevo, porque no digito un número");
            }
        } while (ocurrioUnaBronca);

        return resultado;
    }

    /**
     * Este método permite la lectura de un String (texto).
     * 
     * @param texto Es el texto utilizado como etiqueta para que el usuario sepa que
     *              se le solicita.
     *              Si no desea imprimir una etiqueta, coloque "".
     * @return String (texto) digitado por el usuario.
     */
    public static String leerString(String texto) {
        String resultado = null;
        out.print(texto);

        try {
            resultado = in.readLine();

        } catch (Exception e) {
        }

        return resultado;
    }

    /**
     * Este método permite la lectura de un caracter (texto).
     * Si el usuario digite más de un caracter, toma el primero.
     * NO PUEDE LEER ESPACIOS EN BLANCO, DADO QUE LIMPIA TODOS LOS ESPACIOS.
     * 
     * @param texto Es el texto utilizado como etiqueta para que el usuario sepa que
     *              se le solicita.
     *              Si no desea imprimir una etiqueta, coloque "".
     * @return char (caracter) digitado por el usuario.
     */
    public static char leerCaracter(String texto) {
        String resultado = null;
        out.print(texto);

        try {
            resultado = in.readLine();

        } catch (Exception e) {
        }

        char salida = resultado.trim().charAt(0);

        return salida;
    }

    /**
     * Este método leer un boolean (true/false), para esto se hace una pregunta de
     * tipo Si y NO,
     * si el usuario escribe un Si, el sistema devuelve un true, el usuario escoge
     * No el sistema
     * devuelve un false. Si no responde a las opciones, el sistema sigue
     * preguntando.
     * 
     * @param pregunta Es el texto de la pregunta, no es necesario colocar los
     *                 signos de puntuación.
     * @return boolean que corresopnde a la respuesta del usuario True para Si,
     *         False para No
     */
    public static boolean leerBoolean(String pregunta) {
        char resultado = Character.UNASSIGNED;
        boolean ocurrioUnaBronca = false;

        out.printf("¿%s? \n\tDigite S para Si, N para No, luego presione ENTER\n", pregunta);

        do {
            try {
                resultado = in.readLine().trim().toUpperCase().charAt(0);
                ocurrioUnaBronca = false;
                if (!(resultado == 'S' || resultado == 'N')) {
                    throw new Exception();
                }
            } catch (Exception e) {
                ocurrioUnaBronca = true;
                out.println("Intente de nuevo, Digite S para Si, N para No, luego presione ENTER");
            }
        } while (ocurrioUnaBronca);

        return resultado == 'S';
    }

    /**
     * Este método permite la lectura de un número doble. Si el usuario digita algo
     * que genere un
     * error, el sistema contniuará solicitando el valor correcto.
     * 
     * @param texto Es el texto utilizado como etiqueta para que el usuario sepa que
     *              se le solicita.
     *              Si no desea imprimir una etiqueta, coloque "".
     * @return Número doble digitado por el usuario.
     */
    public static double leerDoble(String texto) {
        double resultado = 0;
        out.print(texto);

        boolean ocurrioUnaBronca = false;

        do {
            try {
                resultado = Double.parseDouble(in.readLine());
                ocurrioUnaBronca = false;
            } catch (Exception e) {
                ocurrioUnaBronca = true;
                out.println("Intente de nuevo, porque no digito un número");
            }
        } while (ocurrioUnaBronca);

        return resultado;
    }

    /**
     * Este método valida la lectura de un rango de valores enteros, ambos límites
     * inclusive.
     * Si el usuario digita un valor fuera del rango, el sistema le solitará otro
     * valor hasta
     * encontrar un valor válido.
     * 
     * @param etiqueta Es el texto utilizado como etiqueta para que el usuario sepa
     *                 que se le solicita.
     * @param min      Valor mínimo del rango
     * @param max      Valor máximo del rango
     * @return Número entero digitado por el usuario.
     */
    public static int leerRangosEnteros(String etiqueta, int min, int max) {
        int resultado = 0;
        out.println(etiqueta);

        do {
            resultado = leerEntero("");
            if (resultado < min || resultado > max) {
                out.println("Valor fuera del rango [" + min + " al " + max + "], digite de nuevo");
            }

        } while (resultado < min || resultado > max);

        return resultado;
    }

    /**
     * Este método valida la lectura de un rango de valores dobles, ambos límites
     * inclusive.
     * Si el usuario digita un valor fuera del rango, el sistema le solitará otro
     * valor hasta
     * encontrar un valor válido.
     * 
     * @param etiqueta Es el texto utilizado como etiqueta para que el usuario sepa
     *                 que se le solicita.
     * @param min      Valor mínimo del rango
     * @param max      Valor máximo del rango
     * @return Número doble digitado por el usuario.
     */
    public static double leerRangosDobles(String etiqueta, double min, double max) {
        double resultado = 0;
        out.println(etiqueta);

        do {
            resultado = leerEntero("");
            if (resultado < min || resultado > max) {
                out.println("Valor fuera del rango [" + min + " al " + max + "], digite de nuevo");
            }

        } while (resultado < min || resultado > max);

        return resultado;
    }

    /**
     * Limpia la consola (en algunas terminales solo generar un bloque sin contenido antes)
     */
    public static void limpiarConsola() {
        System.out.print("\033[2J");
    }

    /**
     * Genera un numero entre un rango de valores, ambos límites inclusive.
     * @param inferior Valor inferior del límite
     * @param superior Valor superior del límite
     * @return Número entero generado aleatoriamente
     */
    public static int generarNumerosEntre(int inferior, int superior) {
        int rango = Math.max(inferior, superior) - Math.min(inferior, superior);
        return Math.min(inferior, superior) + generarNumeroAleatorio(rango);
    }

    /**
     * Genera un número aleatorio entre 0 - n (ambos límites inclusive)
     * @param n Valor límite máximo
     * @return Número entero generado aleatorimente
     */
    public static int generarNumeroAleatorio(int n) {
        // 0 - n (ambos inclusive)
        return (int) Math.round(Math.random() * n);
    }

    public static void establecerColorRojo() {
        System.out.print("\033[31m");
    }

    public static void establecerColorVerde() {
        System.out.print("\033[32m");
    }

    public static void establecerColorAmarillo() {
        System.out.print("\033[33m");
    }

    public static void establecerColorAzul() {
        System.out.print("\033[34m");
    }

    public static void establecerColorMangenta() {
        System.out.print("\033[35m");
    }

    public static void establecerColorCian() {
        System.out.print("\033[36m");
    }

    public static void establecerColorBlanco() {
        System.out.print("\033[37m");
    }

    public static void pausar() {
        System.out.println("Presione <Enter> para continuar...");
        try {
          System.in.read();
        } catch (Exception e) {
    
        }
      }

    public static void reiniciarColores() {
        System.out.print("\033[0m");
    }

    public static void establecerFondoColorBlanco() {
        System.out.print("\033[47m");
    }

    public static void establecerFondoColorRojo() {
        System.out.print("\033[41m");
    }

    public static void establecerFondoColorVerde() {
        System.out.print("\033[42m");
    }

    public static void establecerFondoColorAmarillo() {
        System.out.print("\033[43m");
    }

    public static void establecerFondoColorAzul() {
        System.out.print("\033[44m");
    }

    public static void establecerFondoColorMangenta() {
        System.out.print("\033[45m");
    }

    public static void establecerFondoColorCian() {
        System.out.print("\033[46m");
    }

    public static void establecerFondoColorNegro() {
        System.out.print("\033[40m");
    }

    /**
     * Esta función permite escribir archivos de texto
     * @param nombreArchivo nombre del archivo, se recomienda poner .txt al final
     * para que se guarde con la extensión de texto. Si no pone extensión, el 
     * archivo se guarda sin esta y el sistema operativo no sabe con que asociarlo
     * para abrirlo.
     * @param contenido Es la variable que contiene el texto a escribir el archivo.
     */
    public static void escribirArchivo(String nombreArchivo, String contenido) {
        try (PrintWriter escritor = new PrintWriter(nombreArchivo)) {
            escritor.print(contenido);
        } catch (IOException e) {
            System.err.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }

}

enum Fondo {
    // Color end string, color reset
    RESET("\033[0m"),

    // Background
    NEGRO_BACKGROUND("\033[40m"), // NEGRO
    ROJO_BACKGROUND("\033[41m"), // ROJO
    VERDE_BACKGROUND("\033[42m"), // VERDE
    AMARILLO_BACKGROUND("\033[43m"), // AMARILLO
    AZUL_BACKGROUND("\033[44m"), // AZUL
    MAGENTA_BACKGROUND("\033[45m"), // MAGENTA
    CYAN_BACKGROUND("\033[46m"), // CYAN
    BLANCO_BACKGROUND("\033[47m"), // BLANCO

    // High Intensity backgrounds
    NEGRO_BACKGROUND_INTENSO("\033[0;100m"), // NEGRO
    ROJO_BACKGROUND_INTENSO("\033[0;101m"), // ROJO
    VERDE_BACKGROUND_INTENSO("\033[0;102m"), // VERDE
    AMARILLO_BACKGROUND_INTENSO("\033[0;103m"), // AMARILLO
    AZUL_BACKGROUND_INTENSO("\033[0;104m"), // AZUL
    MAGENTA_BACKGROUND_INTENSO("\033[0;105m"), // MAGENTA
    CYAN_BACKGROUND_INTENSO("\033[0;106m"), // CYAN
    BLANCO_BACKGROUND_INTENSO("\033[0;107m"); // BLANCO

    private final String valor;

    Fondo(String valor) {
        this.valor = valor;
    }

    public String getValor() {
        return valor;
    }

    @Override
    public String toString() {
        return valor;
    }
}

enum Color {
    // Color end string, color reset
    RESET("\033[0m"),

    // Regular Colors. Normal color, no NEGRITA, background color etc.
    NEGRO("\033[0;30m"), // NEGRO
    ROJO("\033[0;31m"), // ROJO
    VERDE("\033[0;32m"), // VERDE
    AMARILLO("\033[0;33m"), // AMARILLO
    AZUL("\033[0;34m"), // AZUL
    MAGENTA("\033[0;35m"), // MAGENTA
    CYAN("\033[0;36m"), // CYAN
    BLANCO("\033[0;37m"), // BLANCO

    // NEGRITA
    NEGRO_NEGRITA("\033[1;30m"), // NEGRO
    ROJO_NEGRITA("\033[1;31m"), // ROJO
    VERDE_NEGRITA("\033[1;32m"), // VERDE
    AMARILLO_NEGRITA("\033[1;33m"), // AMARILLO
    AZUL_NEGRITA("\033[1;34m"), // AZUL
    MAGENTA_NEGRITA("\033[1;35m"), // MAGENTA
    CYAN_NEGRITA("\033[1;36m"), // CYAN
    BLANCO_NEGRITA("\033[1;37m"), // BLANCO

    // Underline
    NEGRO_SUBRAYADO("\033[4;30m"), // NEGRO
    ROJO_SUBRAYADO("\033[4;31m"), // ROJO
    VERDE_SUBRAYADO("\033[4;32m"), // VERDE
    AMARILLO_SUBRAYADO("\033[4;33m"), // AMARILLO
    AZUL_SUBRAYADO("\033[4;34m"), // AZUL
    MAGENTA_SUBRAYADO("\033[4;35m"), // MAGENTA
    CYAN_SUBRAYADO("\033[4;36m"), // CYAN
    BLANCO_SUBRAYADO("\033[4;37m"), // BLANCO

    // High Intensity
    NEGRO_INTENSO("\033[0;90m"), // NEGRO
    ROJO_INTENSO("\033[0;91m"), // ROJO
    VERDE_INTENSO("\033[0;92m"), // VERDE
    AMARILLO_INTENSO("\033[0;93m"), // AMARILLO
    AZUL_INTENSO("\033[0;94m"), // AZUL
    MAGENTA_INTENSO("\033[0;95m"), // MAGENTA
    CYAN_INTENSO("\033[0;96m"), // CYAN
    BLANCO_INTENSO("\033[0;97m"), // BLANCO

    // NEGRITA High Intensity
    NEGRO_NEGRITA_INTENSO("\033[1;90m"), // NEGRO
    ROJO_NEGRITA_INTENSO("\033[1;91m"), // ROJO
    VERDE_NEGRITA_INTENSO("\033[1;92m"), // VERDE
    AMARILLO_NEGRITA_INTENSO("\033[1;93m"), // AMARILLO
    AZUL_NEGRITA_INTENSO("\033[1;94m"), // AZUL
    MAGENTA_NEGRITA_INTENSO("\033[1;95m"), // MAGENTA
    CYAN_NEGRITA_INTENSO("\033[1;96m"), // CYAN
    BLANCO_NEGRITA_INTENSO("\033[1;97m"); // BLANCO

    private final String valor;

    Color(String valor) {
        this.valor = valor;
    }

    public String getValor() {
        return valor;
    }

    @Override
    public String toString() {
        return valor;
    }
}
