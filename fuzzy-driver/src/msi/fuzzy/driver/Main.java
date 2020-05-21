package msi.fuzzy.driver;

import msi.fuzzy.driver.simulator.SimulatorWindow;
import msi.fuzzy.driver.solver.Solver;
import net.sourceforge.jFuzzyLogic.rule.Variable;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) {
        Solver solver = new Solver("phototrap.fcl");

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        boolean continueReading = true;
        SimulatorWindow simulatorWindow = null;

        while (continueReading) {
            try {
                System.out.println("Choose the right option:\n\tsimulate - execute simulation\n\tcharts - draw charts for fuzzy sets\n\tsingle - single calculation\n\tq - exit");
                String input = reader.readLine();

                if (input.equalsIgnoreCase("simulate")) {
                    simulatorWindow = new SimulatorWindow(solver);
                    simulatorWindow.setVisible(true);
                } else if (input.equalsIgnoreCase("charts")) {
                    solver.drawCharts();
                } else if (input.equalsIgnoreCase("single")) {
                    System.out.print("Enter distance from phototrap: ");
                    double distance = Double.parseDouble(reader.readLine());

                    System.out.print("Enter weight of an object: ");
                    double weight = Double.parseDouble(reader.readLine());

                    System.out.print("Enter loudness of an object: ");
                    double loudness = Double.parseDouble(reader.readLine());

                    Variable action = solver.getAction(distance, weight, loudness);
                    System.out.println("Received value: " + action.getValue());
                    solver.showActionChart(action);
                } else if (input.equalsIgnoreCase("q")) {
                    continueReading = false;

                    if (simulatorWindow != null) {
                        simulatorWindow.killSimulationProcess();
                    }
                } else
                    System.out.println("Unrecognized command");
            } catch (IOException e) {
                System.out.println("Error while reading input");
                e.printStackTrace();
            }
        }
    }
}
