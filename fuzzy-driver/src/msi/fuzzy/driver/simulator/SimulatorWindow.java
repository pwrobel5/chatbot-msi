package msi.fuzzy.driver.simulator;

import msi.fuzzy.driver.solver.Solver;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.util.List;
import java.util.Random;

public class SimulatorWindow extends JFrame {
    private boolean runSimulation;
    private int objectX;
    private int objectY;

    private final DisplayGraphics displayGraphics;
    private final ActionListener actionListener;

    private JTextField loudnessTextField;
    private JTextField weightTextField;
    private JTextField xTextField;
    private JTextField yTextField;
    private JTextField speedTextField;

    private double weight;
    private double loudness;
    private int refreshFrequency;

    private final int STEP = 10;
    private final int DISTANCE_THRESHOLD = 150;
    private final int GRAPHICS_WIDTH = 400;
    private final int GRAPHICS_HEIGHT = 500;
    private final int TEXT_FIELD_WIDTH = 10;

    private final Random random = new Random();

    private void getRandomStartingPoint() {
        int axisChoice = random.nextInt(1);
        int sideChoice = random.nextInt(1);
        if (axisChoice == 0) {
            objectX = (sideChoice == 0) ? 0 : GRAPHICS_WIDTH;
            objectY = random.nextInt(GRAPHICS_HEIGHT);
        } else {
            objectY = (sideChoice == 0) ? 0 : GRAPHICS_HEIGHT;
            objectX = random.nextInt(GRAPHICS_WIDTH);
        }
    }

    private double getDistanceFromOrigin(int value, int maxValue) {
        if (value < maxValue)
            return value;
        else
            return maxValue - value;
    }

    public void killSimulationProcess() {
        runSimulation = false;
    }

    public SimulatorWindow(Solver solver) {
        super("Fuzzy Driver Simulation");
        setBounds(101, 101, 400, 400);
        setResizable(false);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        runSimulation = false;
        objectX = 0;
        objectY = 0;
        weight = 20.0;
        loudness = 20.0;
        refreshFrequency = 1000;
        actionListener = getActionListener();
        displayGraphics = new DisplayGraphics(GRAPHICS_WIDTH, GRAPHICS_HEIGHT, solver);

        getContentPane().add(getMainPanel());
        pack();
    }

    private ActionListener getActionListener() {
        return e -> {
            String command = e.getActionCommand();
            if (command.equalsIgnoreCase("start")) {
                runSimulation = true;

                Runnable runnable = () -> {
                    while (runSimulation) {
                        if (getDistanceFromOrigin(objectX, GRAPHICS_WIDTH) < DISTANCE_THRESHOLD) {
                            objectX += random.nextInt(STEP);
                        } else {
                            int sign = random.nextInt(2) - 1;
                            objectX += (sign < 0 ? -1 : 1) * STEP;
                        }

                        if (getDistanceFromOrigin(objectY, GRAPHICS_HEIGHT) < DISTANCE_THRESHOLD) {
                            objectY += random.nextInt(STEP);
                        } else {
                            int sign = random.nextInt(2) - 1;
                            objectY += (sign < 0 ? -1 : 1) * STEP;
                        }

                        if (objectX > GRAPHICS_WIDTH || objectY > GRAPHICS_HEIGHT || objectX < 0 || objectY < 0) {
                            getRandomStartingPoint();
                        } else {
                            displayGraphics.updateObjectPosition(objectX, objectY, weight, loudness);
                        }

                        try {
                            Thread.sleep(refreshFrequency);
                        } catch (InterruptedException e1) {
                            e1.printStackTrace();
                        }
                    }
                };
                Thread thread = new Thread(runnable);
                thread.start();

            } else if (command.equalsIgnoreCase("stop")) {
                runSimulation = false;
            } else if (command.equalsIgnoreCase("change_parameters")) {
                weight = Double.parseDouble(weightTextField.getText());
                loudness = Double.parseDouble(loudnessTextField.getText());
            } else if (command.equalsIgnoreCase("set_coordinates")) {
                objectX = Integer.parseInt(xTextField.getText());
                objectY = Integer.parseInt(yTextField.getText());
            } else if (command.equalsIgnoreCase("set_frequency")) {
                refreshFrequency = Integer.parseInt(speedTextField.getText());
            }
        };
    }

    private JPanel getMainPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints gridConstraints = new GridBagConstraints();

        gridConstraints.gridx = 0;
        gridConstraints.gridy = 0;

        List<Component> components = List.of(getParametersPanel(), displayGraphics, getCoordinatesPanel(), getSpeedPanel(), getButtonPanel());
        for (Component component : components) {
            panel.add(component, gridConstraints);
            gridConstraints.gridy += 1;
        }

        return panel;
    }

    private JPanel getParametersPanel() {
        JPanel parametersPanel = new JPanel();
        parametersPanel.setLayout(new BoxLayout(parametersPanel, BoxLayout.PAGE_AXIS));
        JLabel weightLabel = new JLabel("Weight:");
        parametersPanel.add(weightLabel);
        weightTextField = new JTextField(String.valueOf(weight));
        weightTextField.setColumns(TEXT_FIELD_WIDTH);
        parametersPanel.add(weightTextField);

        JLabel loudnessLabel = new JLabel("Loudness:");
        parametersPanel.add(loudnessLabel);
        loudnessTextField = new JTextField(String.valueOf(loudness));
        loudnessTextField.setColumns(TEXT_FIELD_WIDTH);
        parametersPanel.add(loudnessTextField);

        JButton changeParametersButton = new JButton("Set parameters");
        changeParametersButton.setActionCommand("change_parameters");
        changeParametersButton.addActionListener(actionListener);
        parametersPanel.add(changeParametersButton);

        return parametersPanel;
    }

    private JPanel getCoordinatesPanel() {
        JPanel setCoordinatesPanel = new JPanel();
        JLabel xLabel = new JLabel("x:");
        setCoordinatesPanel.add(xLabel);
        xTextField = new JTextField(String.valueOf(objectX));
        xTextField.setColumns(TEXT_FIELD_WIDTH);
        setCoordinatesPanel.add(xTextField);

        JLabel yLabel = new JLabel("y:");
        setCoordinatesPanel.add(yLabel);
        yTextField = new JTextField(String.valueOf(objectY));
        yTextField.setColumns(TEXT_FIELD_WIDTH);
        setCoordinatesPanel.add(yTextField);

        JButton setCoordinatesButton = new JButton("Set coordinates");
        setCoordinatesButton.setActionCommand("set_coordinates");
        setCoordinatesButton.addActionListener(actionListener);
        setCoordinatesPanel.add(setCoordinatesButton);

        return setCoordinatesPanel;
    }

    private JPanel getSpeedPanel() {
        JPanel speedPanel = new JPanel();
        JLabel speedLabel = new JLabel("Refresh frequency:");
        speedPanel.add(speedLabel);
        speedTextField = new JTextField(String.valueOf(refreshFrequency));
        speedPanel.add(speedTextField);
        JLabel millisecondsLabel = new JLabel("ms");
        speedPanel.add(millisecondsLabel);

        JButton speedButton = new JButton("Set frequency");
        speedButton.setActionCommand("set_frequency");
        speedButton.addActionListener(actionListener);
        speedPanel.add(speedButton);

        return speedPanel;
    }

    private JPanel getButtonPanel() {
        JPanel buttonPanel = new JPanel();
        JButton startButton = new JButton("Start");
        startButton.setActionCommand("start");
        startButton.addActionListener(actionListener);
        buttonPanel.add(startButton);

        JButton stopButton = new JButton("Stop");
        stopButton.setActionCommand("stop");
        stopButton.addActionListener(actionListener);
        buttonPanel.add(stopButton);

        return buttonPanel;
    }
}
