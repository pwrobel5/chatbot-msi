package msi.fuzzy.driver.simulator;

import msi.fuzzy.driver.solver.Solver;
import net.sourceforge.jFuzzyLogic.rule.Variable;

import javax.swing.*;
import javax.swing.border.LineBorder;
import java.awt.*;

public class DisplayGraphics extends JPanel {

    private final int width;
    private final int height;

    private final Color COLOR_NO_OPERATION = Color.GREEN;
    private final Color COLOR_PHOTO = Color.YELLOW;
    private final Color COLOR_ALARM = Color.RED;

    private int objectX;
    private int objectY;
    private int trapX;
    private int trapY;

    private Color currentTrapColor;
    private final Solver solver;

    public DisplayGraphics(int width, int height, Solver solver) {
        this.width = width;
        this.height = height;
        this.objectX = 0;
        this.objectY = 0;
        this.currentTrapColor = COLOR_NO_OPERATION;
        this.solver = solver;

        setPreferredSize(new Dimension(width, height));
        setBorder(new LineBorder(Color.BLACK));
        setBackground(Color.WHITE);
    }

    private Color determineColor(Variable action) {
        double actionValue = action.getValue();

        if (actionValue < 4.0) {
            return COLOR_NO_OPERATION;
        } else if (actionValue >= 4.0 && actionValue < 8.0) {
            return COLOR_PHOTO;
        } else {
            return COLOR_ALARM;
        }
    }

    private double getDistanceFromTrap() {
        double xDiff = objectX - trapX;
        double yDiff = objectY - trapY;

        return Math.sqrt(xDiff * xDiff + yDiff * yDiff);
    }

    public void updateObjectPosition(int x, int y, double weight, double loudness) {
        objectX = x;
        objectY = y;

        double distance = getDistanceFromTrap();
        Variable action = solver.getAction(distance, weight, loudness);
        currentTrapColor = determineColor(action);

        repaint();
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        int OVAL_WIDTH = 10;
        int OVAL_HEIGHT = 10;

        trapX = width / 2;
        trapY = height / 2;

        g.setColor(Color.BLACK);
        if (COLOR_NO_OPERATION.equals(currentTrapColor)) {
            g.drawString("No operation", width / 2, 20);
        } else if (COLOR_PHOTO.equals(currentTrapColor)) {
            g.drawString("Make photo", width / 2, 20);
        } else {
            g.drawString("Alarm", width / 2, 20);
        }

        g.setColor(currentTrapColor);
        g.fillOval(trapX, trapY, OVAL_WIDTH, OVAL_HEIGHT);

        g.setColor(Color.BLACK);
        g.fillOval(objectX, objectY, OVAL_WIDTH, OVAL_HEIGHT);
    }
}
