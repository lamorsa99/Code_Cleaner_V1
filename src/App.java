import utilitarios.Utils;

public class App {
    public static void main(String[] args) throws Exception {
        System.out.println("Hello, World!");
        Utils.establecerColorRojo();
        System.out.println("Hello, World!");
        Utils.establecerColorAzul();
        System.out.println("Hello, World!");
        Utils.reiniciarColores();
    }
}
