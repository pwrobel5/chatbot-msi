package msi.fuzzy.driver.simulator;

import msi.fuzzy.driver.solver.Solver;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

public class SimulatorWindow extends JFrame {
    private boolean runSimulation;
    private int objectX;
    private int objectY;
    private final DisplayGraphics displayGraphics;

    private final JTextField loudnessTextField;
    private final JTextField weightTextField;
    private final JTextField xTextField;
    private final JTextField yTextField;

    private double weight;
    private double loudness;

    private final int STEP = 10;
    private final int DISTANCE_THRESHOLD = 150;
    private final Random random = new Random();

    private void getRandomStartingPoint() {
        objectX = random.nextInt(getWidth());
        objectY = random.nextInt(getHeight());
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

        int TEXT_FIELD_WIDTH = 10;

        ActionListener actionListener = new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String command = e.getActionCommand();
                if (command.equalsIgnoreCase("start")) {
                    runSimulation = true;

                    Runnable runnable = () -> {
                        while (runSimulation) {
                            if (getDistanceFromOrigin(objectX, getWidth()) < DISTANCE_THRESHOLD) {
                                objectX += random.nextInt(STEP);
                            } else {
                                int sign = random.nextInt(2) - 1;
                                objectX += (sign < 0 ? -1 : 1) * STEP;
                            }

                            if (getDistanceFromOrigin(objectY, getHeight()) < DISTANCE_THRESHOLD) {
                                objectY += random.nextInt(STEP);
                            } else {
                                int sign = random.nextInt(2) - 1;
                                objectY += (sign < 0 ? -1 : 1) * STEP;
                            }

                            if (objectX > getWidth() || objectY > getHeight() || objectX < 0 || objectY < 0) {
                                getRandomStartingPoint();
                            } else {
                                displayGraphics.updateObjectPosition(objectX, objectY, weight, loudness);
                            }

                            try {
                                Thread.sleep(1000);
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
                }
            }
        };

        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints gridConstraints = new GridBagConstraints();

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

        gridConstraints.gridx = 0;
        gridConstraints.gridy = 0;
        panel.add(parametersPanel, gridConstraints);

        displayGraphics = new DisplayGraphics(400, 400, solver);
        gridConstraints.gridy = 1;
        panel.add(displayGraphics, gridConstraints);

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

        gridConstraints.gridy = 2;
        panel.add(setCoordinatesPanel, gridConstraints);

        JPanel buttonPanel = new JPanel();
        JButton startButton = new JButton("Start");
        startButton.setActionCommand("start");
        startButton.addActionListener(actionListener);
        buttonPanel.add(startButton);

        JButton stopButton = new JButton("Stop");
        stopButton.setActionCommand("stop");
        stopButton.addActionListener(actionListener);
        buttonPanel.add(stopButton);

        gridConstraints.gridy = 3;
        panel.add(buttonPanel, gridConstraints);

        getContentPane().add(panel);
        pack();
    }
}
